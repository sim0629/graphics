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
        private Sphere sphere;

        public SimpleSphere(Phong material, Point3D center, double radius)
        {
            this.Material = material;
            this.sphere = new Sphere(center, radius);
        }

        public override bool Intersects(Ray ray, out Point3D intersection)
        {
            return Geometry.Intersects(ray, this.sphere, out intersection);
        }

        public override Vector3D NormalAt(Point3D point)
        {
            return this.sphere.NormalAt(point);
        }
    }
}
