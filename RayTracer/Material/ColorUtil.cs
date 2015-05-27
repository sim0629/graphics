using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;

namespace Gyumin.Graphics.RayTracer.Material
{
    public static class ColorUtil
    {
        public static Color ElementWiseMultiply(Color lhs, Color rhs)
        {
            return Color.FromRgb(
                (byte)((int)lhs.R * rhs.R / 255),
                (byte)((int)lhs.G * rhs.G / 255),
                (byte)((int)lhs.B * rhs.B / 255));
        }
    }
}
