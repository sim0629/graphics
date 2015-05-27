using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.Model
{
    using Material;
    using MathUtil;

    public class Rectangle : Renderable
    {
        private Polygon polygon;

        public Rectangle(Point3D p0, Point3D p1, Point3D p2, Point3D p3, Phong material)
        {
            this.polygon = new Polygon(p0, p1, p2, p3);
            this.Material = material;
        }

        public override bool Intersects(Ray ray, out Point3D intersection)
        {
            return Geometry.Intersects(ray, this.polygon, out intersection);
        }

        public override Vector3D NormalAt(Point3D point)
        {
            return this.polygon.Plane.Normal;
        }
    }
}
