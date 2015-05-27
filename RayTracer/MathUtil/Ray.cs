using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.MathUtil
{
    using Model;

    public class Ray
    {
        public Point3D Position { get; private set; }

        public Vector3D Direction { get; private set; }

        public Ray(Point3D position, Vector3D direction)
        {
            direction.Normalize();
            this.Position = position;
            this.Direction = direction;
        }
    }
}
