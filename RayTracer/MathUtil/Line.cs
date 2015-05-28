using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.MathUtil
{
    public class Line
    {
        public Point3D Start { get; private set; }

        public Point3D End { get; private set; }

        private double? length;

        public double Length
        {
            get
            {
                if (this.length == null)
                {
                    this.length = (this.End - this.Start).Length;
                }
                return this.length.Value;
            }
        }

        private Ray ray;

        public Ray Ray
        {
            get
            {
                if (this.ray == null)
                {
                    var v = this.End - this.Start;
                    this.ray = new Ray(this.Start, v);
                }
                return this.ray;
            }
        }

        public Line(Point3D start, Point3D end)
        {
            this.Start = start;
            this.End = end;
        }
    }
}
