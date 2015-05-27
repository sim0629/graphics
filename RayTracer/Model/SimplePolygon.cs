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

    public class SimplePolygon : Renderable
    {
        protected Polygon polygon;

        public SimplePolygon(Phong material, params Point3D[] points)
        {
            this.Material = material;
            this.polygon = new Polygon(points);
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
