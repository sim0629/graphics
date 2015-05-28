using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.Model
{
    using Material;
    using MathUtil;

    public class Sphere : Renderable
    {
        private Point3D center;

        private double radius;

        private double radius2;

        public Sphere(Phong material, Point3D center, double radius)
        {
            this.Material = material;
            this.center = center;
            this.radius = radius;
            this.radius2 = radius * radius;
        }

        public override bool Intersects(Ray ray, out Point3D intersection)
        {
            var to_center = this.center - ray.Position;
            var to_foot_len = Vector3D.DotProduct(to_center, ray.Direction);
            var to_foot_len2 = to_foot_len * to_foot_len;
            var distance2 = to_center.LengthSquared - to_foot_len2;
            if (Geometry.GreaterOrEqual(distance2, radius2))
            {
                intersection = new Point3D();
                return false;
            }
            var offset2 = radius2 - distance2;
            if (Geometry.IsZero(offset2))
            {
                intersection = ray.Position + to_foot_len * ray.Direction;
            }
            else
            {
                var offset = Math.Sqrt(offset2);
                intersection = ray.Position + (to_foot_len - offset) * ray.Direction;
            }
            return true;
        }

        public override Vector3D NormalAt(Point3D point)
        {
            var normal = point - this.center;
            Debug.Assert(Geometry.IsZero(normal.Length - this.radius));
            normal.Normalize();
            return normal;
        }
    }
}
