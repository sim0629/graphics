using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Media.Media3D;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Gyumin.Graphics.RayTracer
{
    using Material;
    using Model;

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private Scene scene;

        private int progress_value;

        private string stl_file;

        private Random random = new Random();

        public MainWindow()
        {
            InitializeComponent();

            this.Unloaded += (sender, e) => { Application.Current.Shutdown(); };
            this.xStart.Click += xStart_Click;
            this.xImport.Click += xImport_Click;
            this.xExport.Click += xExport_Click;
        }

        private async void xStart_Click(object sender, RoutedEventArgs e)
        {
            this.xMenu.IsEnabled = false;
            this.ConstructScene();
            this.xImage.Source = await this.RenderSceneAsync(Config.ImageWidth, Config.ImageHeight, Config.NumberOfWorkers, this.xAntiAliasing.IsChecked);
            this.xMenu.IsEnabled = true;
        }

        private void xImport_Click(object sender, RoutedEventArgs e)
        {
            this.stl_file = FileUtil.OpenStl();
            this.xTextBlock.Text = this.stl_file;
        }

        private void xExport_Click(object sender, RoutedEventArgs e)
        {
            FileUtil.SaveToPng(this.xImage.Source as BitmapSource);
        }

        private void ConstructScene()
        {
            this.scene = new Scene(Colors.DeepSkyBlue);

            if (!this.xSoftShadow.IsChecked)
            {
                var bulb = new PointLight(
                    new Point3D(0, 0.5, -0.5),
                    Color.FromRgb(200, 200, 200),
                    Colors.Black);
                scene.AddLight(bulb);
            }
            else
            {
                for (var i = -2; i <= 2; i++)
                {
                    for (var j = -2; j <= 2; j++)
                    {
                        var bulb = new PointLight(
                            new Point3D(0 + 0.05 * i, 0.5, -0.5 + 0.05 * j),
                            Color.FromRgb(32, 32, 32),
                            Colors.Black);
                        scene.AddLight(bulb);
                    }
                }
            }

            var sun = new DirectionalLight(
                new Vector3D(1, -1.3, 1),
                Colors.White,
                Color.FromRgb(200, 200, 200));
            scene.AddLight(sun);

            var concrete = new Phong(
                Color.FromRgb(50, 50, 50),
                Color.FromRgb(150, 150, 150),
                Colors.White, 5,
                0, 0, 1);

            var mirror = new Phong(
                Color.FromRgb(32, 32, 32),
                Colors.Black,
                Colors.White, 100,
                0.9, 0, 1);

            var glass = new Phong(
                Colors.Black,
                Colors.White,
                Colors.White, 100,
                0.1, 0.9, 1.52);

            var royal = new Phong(
                Colors.RoyalBlue,
                Colors.RoyalBlue,
                Colors.RoyalBlue, 100,
                0, 0.6, 1.52);

            var orange = new Phong(
                Colors.OrangeRed,
                Colors.OrangeRed,
                Colors.OrangeRed, 100,
                0, 0.6, 1.52);

            var marble = new Phong(
                Color.FromRgb(50, 50, 50),
                Colors.Beige,
                Colors.White, 20,
                0.15, 0, 1.6);

            var floor = new SimplePolygon(
                marble,
                new Point3D(1, -0.75, 1),
                new Point3D(1, -0.75, -1),
                new Point3D(-1, -0.75, -1),
                new Point3D(-1, -0.75, 1)
            );
            scene.AddObject(floor);

            var ceiling = new SimplePolygon(
                concrete,
                new Point3D(-1, 0.75, 1),
                new Point3D(-1, 0.75, -1),
                new Point3D(1, 0.75, -1),
                new Point3D(1, 0.75, 1)
            );
            scene.AddObject(ceiling);

            var right_wall = new SimplePolygon(
                concrete,
                new Point3D(1, -0.75, 1),
                new Point3D(1, 0.75, 1),
                new Point3D(1, 0.75, -1),
                new Point3D(1, -0.75, -1)
            );
            scene.AddObject(right_wall);

            var left_wall = new SimplePolygon(
                mirror,
                new Point3D(-1, -0.75, -1),
                new Point3D(-1, 0.75, -1),
                new Point3D(-1, 0.75, 1),
                new Point3D(-1, -0.75, 1)
            );
            scene.AddObject(left_wall);

            var back_wall_ur = new SimplePolygon(
                concrete,
                new Point3D(1, -0.75, -1),
                new Point3D(1, 0.75, -1),
                new Point3D(-1, 0.75, -1),
                new Point3D(-0.5, 0.5, -1),
                new Point3D(0.5, 0.5, -1),
                new Point3D(0.5, -0.2, -1)
            );
            var back_wall_dl = new SimplePolygon(
                concrete,
                new Point3D(-1, 0.75, -1),
                new Point3D(-1, -0.75, -1),
                new Point3D(1, -0.75, -1),
                new Point3D(0.5, -0.2, -1),
                new Point3D(-0.5, -0.2, -1),
                new Point3D(-0.5, 0.5, -1)
            );
            var back_wall_out_u = new SimplePolygon(
                concrete,
                new Point3D(-0.5, 0.5, -1),
                new Point3D(-0.5, 0.5, -1.2),
                new Point3D(0.5, 0.5, -1.2),
                new Point3D(0.5, 0.5, -1)
            );
            var back_wall_out_r = new SimplePolygon(
                concrete,
                new Point3D(0.5, 0.5, -1),
                new Point3D(0.5, 0.5, -1.2),
                new Point3D(0.5, -0.2, -1.2),
                new Point3D(0.5, -0.2, -1)
            );
            var back_wall_out_l = new SimplePolygon(
                concrete,
                new Point3D(-0.5, -0.2, -1),
                new Point3D(-0.5, -0.2, -1.2),
                new Point3D(-0.5, 0.5, -1.2),
                new Point3D(-0.5, 0.5, -1)
            );
            var back_wall_out_d = new SimplePolygon(
                concrete,
                new Point3D(0.5, -0.2, -1),
                new Point3D(0.5, -0.2, -1.2),
                new Point3D(-0.5, -0.2, -1.2),
                new Point3D(-0.5, -0.2, -1)
            );
            scene.AddObject(back_wall_ur);
            scene.AddObject(back_wall_dl);
            scene.AddObject(back_wall_out_u);
            scene.AddObject(back_wall_out_r);
            scene.AddObject(back_wall_out_l);
            scene.AddObject(back_wall_out_d);

            var window = new SimplePolygon(
                glass,
                new Point3D(0.5, 0.5, -1),
                new Point3D(-0.5, 0.5, -1),
                new Point3D(-0.5, -0.2, -1),
                new Point3D(0.5, -0.2, -1)
            );
            scene.AddObject(window);

            var front_wall = new SimplePolygon(
                concrete,
                new Point3D(1, 0.75, 1),
                new Point3D(1, -0.75, 1),
                new Point3D(-1, -0.75, 1),
                new Point3D(-1, 0.75, 1)
            );
            scene.AddObject(front_wall);

            var ball = new SimpleSphere(
                mirror,
                new Point3D(-0.3, -0.5, -0.5),
                0.25
            );
            scene.AddObject(ball);

            var bead_b = new SimpleSphere(
                royal,
                new Point3D(0, -0.65, 0),
                0.1
            );
            scene.AddObject(bead_b);

            var bead_r = new SimpleSphere(
                orange,
                new Point3D(-0.15, -0.65, -0.16),
                0.1
            );
            scene.AddObject(bead_r);

            if (this.stl_file != null)
            {
                var stl = new Mesh(
                    concrete,
                    this.stl_file,
                    new Point3D(0.5, -0.3, -0.6),
                    0.5);
                scene.AddObject(stl);
            }
        }

        private async Task<BitmapSource> RenderSceneAsync(int width, int height, int n, bool anti_aliasing)
        {
            this.Dispatcher.Invoke(() =>
            {
                this.xProgress.Minimum = 0;
                this.xProgress.Maximum = width * height;
                this.xProgress.Value = progress_value = 0;
            });
            var pixels = new byte[3 * width * height];
            var tasks = new List<Task>();
            for (var t = 0; t < n; t++)
            {
                var start_i = (height + n - 1) / n * t;
                var end_i = (height + n - 1) / n * (t + 1);
                var task = new Task(() =>
                {
                    for (var i = start_i; i < end_i && i < height; i++)
                    {
                        for (var j = 0; j < width; j++)
                        {
                            var color = Colors.Black;
                            if (anti_aliasing)
                            {
                                var dx = (double)2 / 3 / width;
                                var dy = (double)2 / 3 / height;
                                for (var x = -1; x <= 1; x++)
                                {
                                    for (var y = -1; y <= 1; y++)
                                    {
                                        var color_k = this.scene.Trace(
                                            (double)(2 * j + 1 - width) / width + dx * x,
                                            (double)(height - 2 * i + 1) / height + dy * y);
                                        color = Color.Add(color, Color.Multiply(color_k, (float)1 / 9));
                                    }
                                }
                            }
                            else
                            {
                                color = this.scene.Trace(
                                    (double)(2 * j + 1 - width) / width,
                                    (double)(height - 2 * i + 1) / height);
                            }
                            var index = 3 * (i * width + j);
                            pixels[index + 0] = color.R;
                            pixels[index + 1] = color.G;
                            pixels[index + 2] = color.B;
                            this.Dispatcher.Invoke(() =>
                            {
                                this.xProgress.Value = ++this.progress_value;
                            });
                        }
                    }
                });
                task.Start();
                tasks.Add(task);
            }
            await Task.WhenAll(tasks);
            this.Dispatcher.Invoke(() =>
            {
                this.xProgress.Value = progress_value = 0;
            });
            return BitmapSource.Create(
                Config.ImageWidth, Config.ImageHeight,
                96, 96,
                PixelFormats.Rgb24, null,
                pixels, 3 * Config.ImageWidth);
        }
    }
}
