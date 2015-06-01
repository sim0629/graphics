using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.Model
{
    using Material;
    using MathUtil;

    public class Scene
    {
        private FloatColor backgroundColor;

        private List<Light> lights = new List<Light>();

        private List<Renderable> objects = new List<Renderable>();

        private Camera camera = new Camera();

        public Scene(FloatColor backgroundColor)
        {
            this.backgroundColor = backgroundColor;
        }

        private Renderable FirstMeet(Ray ray, out Point3D at, Renderable except)
        {
            at = new Point3D();
            var found = this.objects.Where(o => o != except)
                .Select(renderable =>
                {
                    var intersection = new Point3D();
                    var intersects = renderable.Intersects(ray, out intersection);
                    return new { Renderable = renderable, Intersects = intersects, Intersection = intersection };
                })
                .Where(result => result.Intersects)
                .OrderBy(result => (result.Intersection - ray.Position).Length)
                .FirstOrDefault();
            if (found == null)
                return null;
            at = found.Intersection;
            return found.Renderable;
        }

        private FloatColor? TransparentLight(Light light, Point3D at, Renderable except)
        {
            var color = (FloatColor)Colors.White;
            var unused = new Point3D();
            var ray = light.RayFrom(at);
            var distance = light.DistanceFrom(at);
            Line line = null;
            Func<Renderable, bool> check;
            if (double.IsPositiveInfinity(distance))
            {
                check = renderable => renderable.Intersects(ray, out unused);
            }
            else
            {
                line = new Line(ray.Position, ray.Position + distance * ray.Direction);
                check = renderable => renderable.Intersects(line, out unused);
            }
            foreach (var renderable in this.objects.Where(o => o != except))
            {
                if (check(renderable))
                {
                    var k_refraction = renderable.Material.K_Refraction;
                    if (Geometry.IsZero(k_refraction))
                        return null;
                    color &= renderable.Material.Diffuse * (float)k_refraction;
                }
            }
            return color;
        }

        private FloatColor Trace(Ray ray, Renderable except, int depth)
        {
            var at = new Point3D();
            var renderable = this.FirstMeet(ray, out at, except);
            if (renderable == null)
                return this.backgroundColor;

            var color = (FloatColor)Colors.Black;

            var k_a = renderable.Material.Ambient;
            var k_d = renderable.Material.Diffuse;
            var k_s = renderable.Material.Specular;
            var n = renderable.Material.Shininess;

            var normal = renderable.NormalAt(at);

            foreach (var light in this.lights)
            {
                color += k_a & (light.Ambient * (float)(1 - renderable.Material.K_Refraction));

                var to_light = light.RayFrom(at);
                var cos_t = Vector3D.DotProduct(normal, to_light.Direction);
                if (!Geometry.IsZero(renderable.Material.K_Refraction) && cos_t < -Geometry.Epsilon)
                {
                    normal = -normal;
                    cos_t = -cos_t;
                }
                if (cos_t > Geometry.Epsilon)
                {
                    var transparent_light_color = this.TransparentLight(light, at, renderable);
                    if (transparent_light_color != null)
                    {
                        var shadow_light_color = (light.IntensityAt(at) * (float)(1 - renderable.Material.K_Refraction)) & transparent_light_color.Value;

                        color += (k_d & shadow_light_color) * (float)cos_t;

                        var reflected = Vector3D.DotProduct(2 * to_light.Direction, normal) * normal - to_light.Direction;
                        color += (k_s & shadow_light_color) * (float)Math.Pow(Vector3D.DotProduct(reflected, -ray.Direction), n);
                    }
                }
            }

            if (depth >= 5)
                return color;

            var k_reflection = renderable.Material.K_Reflection;
            if (!Geometry.IsZero(k_reflection))
            {
                var reflection_ray = new Ray(at,
                    Vector3D.DotProduct(-2 * ray.Direction, normal) * normal + ray.Direction);
                color += this.Trace(reflection_ray, renderable, depth + 1) * (float)k_reflection;
            }

            var k_refraction = renderable.Material.K_Refraction;
            if (!Geometry.IsZero(k_refraction))
            {
                var refraction_ray = renderable.Refracted(at, ray.Direction);
                color += this.Trace(refraction_ray, renderable, depth + 1) * (float)k_refraction;
            }

            return color;
        }

        public FloatColor Trace(double x, double y)
        {
            var ray = this.camera.GetRayToScreen(x, y);
            return this.Trace(ray, null, 1);
        }

        public void AddLight(Light light)
        {
            this.lights.Add(light);
        }

        public void AddObject(Renderable renderable)
        {
            this.objects.Add(renderable);
        }
    }
}
