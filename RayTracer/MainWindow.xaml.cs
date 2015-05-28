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
        private Scene scene = new Scene(Colors.DeepSkyBlue);

        public MainWindow()
        {
            InitializeComponent();

            this.Loaded += MainWindow_Loaded;
            this.Unloaded += MainWindow_Unloaded;
        }

        private async void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            this.ConstructScene();
            this.xImage.Source = await this.RenderSceneAsync(Config.ImageWidth, Config.ImageHeight, Config.NumberOfWorkers);
        }

        private void MainWindow_Unloaded(object sender, RoutedEventArgs e)
        {
            Application.Current.Shutdown();
        }

        private void ConstructScene()
        {
            var bulb = new PointLight(
                new Point3D(0, 0.5, -0.5),
                Color.FromRgb(200, 200, 200),
                Colors.White);
            scene.AddLight(bulb);

            var sun = new DirectionalLight(
                new Vector3D(1, -1.4, 1),
                Colors.White,
                Colors.Black);
            scene.AddLight(sun);

            var concrete = new Phong(
                Color.FromRgb(50, 50, 50),
                Color.FromRgb(150, 150, 150),
                Colors.White, 5,
                0);

            var mirror = new Phong(
                Color.FromRgb(50, 50, 50),
                Colors.Black,
                Colors.White, 100,
                0.9);

            var floor = new SimplePolygon(
                concrete,
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
        }

        private async Task<BitmapSource> RenderSceneAsync(int width, int height, int n)
        {
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
                            var color = this.scene.Trace(
                                (double)(2 * j + 1 - width) / width,
                                (double)(height - 2 * i + 1) / height);
                            var index = 3 * (i * width + j);
                            pixels[index + 0] = color.R;
                            pixels[index + 1] = color.G;
                            pixels[index + 2] = color.B;
                        }
                    }
                });
                task.Start();
                tasks.Add(task);
            }
            await Task.WhenAll(tasks);
            return BitmapSource.Create(
                Config.ImageWidth, Config.ImageHeight,
                96, 96,
                PixelFormats.Rgb24, null,
                pixels, 3 * Config.ImageWidth);
        }
    }
}
