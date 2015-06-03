using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Media.Media3D;

namespace Gyumin.Graphics.RayTracer.Model
{
    using Material;
    using MathUtil;

    public class TexturedRectangle : SimplePolygon
    {
        private Color[,] texture_pixels;

        public TexturedRectangle(Phong material, Point3D p0, Point3D p1, Point3D p2, Point3D p3, Uri texture_path)
            : base(material, p0, p1, p2, p3)
        {
            this.texture_pixels = BitmapUtil.GetPixels(new BitmapImage(texture_path));
        }

        public override FloatColor DiffuseAt(Point3D point)
        {
            var U = this.polygon[3] - this.polygon[0];
            var V = this.polygon[1] - this.polygon[0];
            var U_len = U.Length;
            var V_len = V.Length;
            U.Normalize();
            V.Normalize();

            var P = point - this.polygon[0];
            var u = Vector3D.DotProduct(P, U) / U_len;
            var v = Vector3D.DotProduct(P, V) / V_len;

            var width = this.texture_pixels.GetLength(0);
            var height = this.texture_pixels.GetLength(1);
            var x = Math.Min(width, Math.Max(0, (int)(u * width)));
            var y = Math.Min(height, Math.Max(0, (int)(v * height)));

            return base.DiffuseAt(point) & (FloatColor)texture_pixels[x, y];
        }
    }
}
