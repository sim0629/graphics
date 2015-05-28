using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.Model
{
    using Material;
    using MathUtil;

    public abstract class Renderable
    {
        public Phong Material { get; protected set; }

        public abstract bool Intersects(Ray ray, out Point3D intersection);

        public virtual bool Intersects(Line line, out Point3D intersection)
        {
            intersection = new Point3D();
            if (this.Intersects(line.Ray, out intersection))
            {
                return Geometry.LessOrEqual((intersection - line.Start).Length, line.Length);
            }
            return false;
        }

        public abstract Vector3D NormalAt(Point3D point);
    }
}
