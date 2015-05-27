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

    public class Rectangle
    {
        private Polygon polygon;

        public Polygon Polygon { get { return this.polygon; } }

        private Phong material;

        public Phong Material { get { return this.material; } }

        public Rectangle(Point3D p0, Point3D p1, Point3D p2, Point3D p3, Phong material)
        {
            this.polygon = new Polygon(p0, p1, p2, p3);
            this.material = material;
        }
    }
}
