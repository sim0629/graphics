using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;

namespace Gyumin.Graphics.RayTracer.Material
{
    public struct FloatColor
    {
        public float R;

        public float G;

        public float B;

        public static FloatColor operator +(FloatColor lhs, FloatColor rhs)
        {
            return new FloatColor()
            {
                R = lhs.R + rhs.R,
                G = lhs.G + rhs.G,
                B = lhs.B + rhs.B,
            };
        }

        public static FloatColor operator -(FloatColor lhs, FloatColor rhs)
        {
            return new FloatColor()
            {
                R = lhs.R - rhs.R,
                G = lhs.G - rhs.G,
                B = lhs.B - rhs.B,
            };
        }

        public static FloatColor operator &(FloatColor lhs, FloatColor rhs)
        {
            return new FloatColor()
            {
                R = lhs.R * rhs.R,
                G = lhs.G * rhs.G,
                B = lhs.B * rhs.B,
            };
        }

        public static FloatColor operator *(FloatColor c, float f)
        {
            return new FloatColor()
            {
                R = c.R * f,
                G = c.G * f,
                B = c.B * f,
            };
        }

        public static FloatColor operator *(float f, FloatColor c)
        {
            return new FloatColor()
            {
                R = c.R * f,
                G = c.G * f,
                B = c.B * f,
            };
        }

        public static FloatColor operator /(FloatColor c, float f)
        {
            return new FloatColor()
            {
                R = c.R / f,
                G = c.G / f,
                B = c.B / f,
            };
        }

        public static explicit operator FloatColor(Color c)
        {
            return new FloatColor()
            {
                R = (float)c.R / 255,
                G = (float)c.G / 255,
                B = (float)c.B / 255,
            };
        }

        public static explicit operator Color(FloatColor c)
        {
            var r = (byte)Math.Max(Math.Min((int)(c.R * 255), 255), 0);
            var g = (byte)Math.Max(Math.Min((int)(c.G * 255), 255), 0);
            var b = (byte)Math.Max(Math.Min((int)(c.B * 255), 255), 0);
            return Color.FromRgb(r, g, b);
        }
    }
}
