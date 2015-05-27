using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.MathUtil
{
    public class Plane
    {
        public Vector3D Normal { get; private set; }

        public double D { get; private set; }

        public Plane(Point3D p0, Vector3D normal)
        {
            normal.Normalize();
            this.Normal = normal;
            this.D = -Vector3D.DotProduct(this.Normal, (Vector3D)p0);
        }

        public Plane(Point3D p0, Point3D p1, Point3D p2)
            : this(p0, Vector3D.CrossProduct(p1 - p0, p2 - p0))
        {
        }
    }
}
