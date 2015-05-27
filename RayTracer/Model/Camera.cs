using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.Model
{
    using MathUtil;

    public class Camera
    {
        private Point3D position = new Point3D(0, 0, 1);

        private Point3D reference = new Point3D(0, 0, 0);

        private Vector3D up = new Vector3D(0, 1, 0);

        private double fov_x = 90;

        private double ratio_xy = 0.75;

        private double near = 1;

        private Coordinate viewing;

        public Coordinate Viewing
        {
            get
            {
                if (this.viewing == null)
                {
                    var n = this.position - this.reference; n.Normalize();
                    var u = Vector3D.CrossProduct(this.up, n); u.Normalize();
                    var v = Vector3D.CrossProduct(n, u);
                    this.viewing = new Coordinate(n, u, v);
                }
                return this.viewing;
            }
        }

        public Camera()
        {
        }

        public Ray GetRayToScreen(double x, double y)
        {
            var half_width = near * Math.Tan(this.fov_x / 2 * Math.PI / 180);
            var half_height = ratio_xy * half_width;
            var direction = -near * this.Viewing.N
                + x * half_width * this.Viewing.U
                + y * half_height * this.Viewing.V;
            return new Ray(this.position, direction);
        }
    }
}
