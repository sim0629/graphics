using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.MathUtil
{
    public class Sphere
    {
        public Point3D Center { get; private set; }

        public double Radius { get; private set; }

        public double Radius2 { get; private set; }

        public Sphere(Point3D center, double radius)
        {
            this.Center = center;
            this.Radius = radius;
            this.Radius2 = radius * radius;
        }

        public Vector3D NormalAt(Point3D point)
        {
            var normal = point - this.Center;
            Debug.Assert(Geometry.IsZero(normal.Length - this.Radius));
            normal.Normalize();
            return normal;
        }
    }
}
