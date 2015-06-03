using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;
using System.Windows.Media.Imaging;

namespace Gyumin.Graphics.RayTracer
{
    public static class BitmapUtil
    {
        public static Color[,] GetPixels(BitmapSource source)
        {
            if (source.Format != PixelFormats.Rgb24)
                source = new FormatConvertedBitmap(source, PixelFormats.Rgb24, null, 0);

            var width = source.PixelWidth;
            var height = source.PixelHeight;
            var pixels = new byte[3 * width * height];

            source.CopyPixels(pixels, 3 * width, 0);

            var result = new Color[width, height];

            for (var j = 0; j < width; j++)
            {
                for (var i = 0; i < height; i++)
                {
                    result[j, i].R = pixels[3 * (i * width + j) + 0];
                    result[j, i].G = pixels[3 * (i * width + j) + 1];
                    result[j, i].B = pixels[3 * (i * width + j) + 2];
                }
            }

            return result;
        }
    }
}
