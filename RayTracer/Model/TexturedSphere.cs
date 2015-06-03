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

    public class TexturedSphere : SimpleSphere
    {
        private Color[,] texture_pixels;

        private Coordinate texture_coord;

        public TexturedSphere(Phong material, Point3D center, double radius, Uri texture_path, Coordinate texture_coord)
            : base(material, center, radius)
        {
            this.texture_pixels = BitmapUtil.GetPixels(new BitmapImage(texture_path));
            this.texture_coord = texture_coord;
        }

        public override FloatColor? TextureColorAt(Point3D point)
        {
            var P = point - this.sphere.Center;

            var n = Vector3D.DotProduct(this.texture_coord.N, P);
            var u = Vector3D.DotProduct(this.texture_coord.U, P);
            var theta = Math.Atan2(u, n);

            var sin_phi = Vector3D.DotProduct(this.texture_coord.V, P) / P.Length;
            var phi = Math.Asin(Math.Min(1, Math.Max(-1, sin_phi)));

            var width = this.texture_pixels.GetLength(0);
            var height = this.texture_pixels.GetLength(1);
            var x = Math.Min(width, Math.Max(0, (int)((theta + Math.PI) / (2 * Math.PI) * width)));
            var y = Math.Min(height, Math.Max(0, (int)((-phi + Math.PI / 2) / Math.PI * height)));

            return (FloatColor)texture_pixels[x, y];
        }
    }
}
