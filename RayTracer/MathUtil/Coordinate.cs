using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.MathUtil
{
    public class Coordinate
    {
        public Vector3D N { get; private set; }

        public Vector3D U { get; private set; }

        public Vector3D V { get; private set; }

        public Coordinate(Vector3D n, Vector3D u, Vector3D v)
        {
            this.N = n;
            this.U = u;
            this.V = v;
        }
    }
}
