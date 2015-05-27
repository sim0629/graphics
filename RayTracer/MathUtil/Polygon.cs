using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.MathUtil
{
    public class Polygon
    {
        private List<Point3D> points = new List<Point3D>();

        public int NumberOfPoints { get { return this.points.Count; } }

        public Point3D this[int index] { get { return this.points[index]; } }

        private Plane plane;

        public Plane Plane
        {
            get
            {
                if (this.plane == null)
                {
                    this.plane = new Plane(this.points[0], this.points[1], this.points[2]);
                }
                return this.plane;
            }
        }

        public Polygon(params Point3D[] points)
        {
            Debug.Assert(points.Length >= 3);
            this.points.AddRange(points);
        }
    }
}
