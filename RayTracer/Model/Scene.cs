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
        private Color backgroundColor = Colors.Black;

        private List<Light> lights = new List<Light>();

        private List<Renderable> objects = new List<Renderable>();

        private Camera camera = new Camera();

        public Scene()
        {
        }

        private Color Trace(Ray ray)
        {
            var intersection = new Point3D();
            if (objects[0].Intersects(ray, out intersection))
            {
                return objects[0].Material.Diffuse;
            }
            else
            {
                return this.backgroundColor;
            }
        }

        public Color Trace(double x, double y)
        {
            var ray = this.camera.GetRayToScreen(x, y);
            return this.Trace(ray);
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
