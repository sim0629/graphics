using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.Model
{
    using Material;
    using MathUtil;

    public class SimpleSphere : Renderable
    {
        protected Sphere sphere;

        public SimpleSphere(Phong material, Point3D center, double radius)
        {
            this.Material = material;
            this.sphere = new Sphere(center, radius);
        }

        public override bool Intersects(Ray ray, out Point3D intersection)
        {
            return Geometry.Intersects(ray, this.sphere, out intersection, false);
        }

        public override Vector3D NormalAt(Point3D point)
        {
            return this.sphere.NormalAt(point);
        }

        public override Ray Refracted(Point3D point, Vector3D direction)
        {
            direction.Normalize();
            var L = -direction;
            var N = this.NormalAt(point);
            var cos_ti = Vector3D.DotProduct(N, L);
            var n = 1 / this.Material.N_Index;
            var cos_tr2 = 1 - n * n * (1 - cos_ti * cos_ti);
            var cos_tr = Geometry.IsZero(cos_tr2) ? 0 : Math.Sqrt(cos_tr2);
            var T = (n * cos_ti - cos_tr) * N - n * L;

            var T_ray = new Ray(point, T);
            if (!Geometry.Intersects(T_ray, this.sphere, out point, true))
                return T_ray;
            T = -T;
            N = this.NormalAt(point);
            cos_ti = Vector3D.DotProduct(N, T);
            n = this.Material.N_Index;
            cos_tr2 = 1 - n * n * (1 - cos_ti * cos_ti);
            cos_tr = Geometry.IsZero(cos_tr2) ? 0 : Math.Sqrt(cos_tr2);
            var U = (n * cos_ti - cos_tr) * N - n * T;

            return new Ray(point, U);
        }

        public void Move()
        {
            this.sphere.Move();
        }
    }
}
