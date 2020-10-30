import javax.swing.*;
import java.awt.*;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintStream;
import java.util.Scanner;

public class Main extends JFrame {
	static final int board_w = 960;
	static final int board_h = 800;
	static final int edge = 25;
	private static final int global_w = board_w + 2 * edge;
	private static final int global_h = board_h + 2 * edge;
	private static final float img_scale = 2.5f;

	private static final String path_result = "result/manual_lines.csv";
	private static final String path_time = "source/time_list.txt";
	private static final String path_format_img = "source/image/%02d_%.4f.jpg";

	static Action action = new Action();

	static void process_init() {
		try {
			System.out.println(">> initiating .. ");
			File file = new File(path_time);
			Scanner fr = new Scanner(file);

			if (!fr.hasNext()) {
				System.err.println(">> empty time list .. ");
				System.exit(-1);
			}

			action.frame_count = 0;
			while (fr.hasNext()) {
				fr.nextLine();
				action.frame_count++;
			}
			double[] time_list = new double[action.frame_count];
			fr = new Scanner(file);
			for (int i = 0; i < action.frame_count; i++) {
				time_list[i] = Double.parseDouble(fr.nextLine());
			}
			fr.close();

			action.img_nodes = new ImgNode[action.frame_count][2];
			for (int i = 0; i < action.frame_count; i++) {
				for (int j = 0; j < 2; j++) {
					int cam_id = j + 1;
					String path = String.format(path_format_img, cam_id, time_list[i]);
					action.img_nodes[i][j] = new ImgNode(time_list[i], cam_id, path);
				}
			}
			action.mouse_pos[0] = global_w / 2;
			action.mouse_pos[1] = global_h / 2;

			System.out.println(">> done .. ");
		} catch (Exception ignored) {
			System.err.println(">> initiation failed .. ");
			System.exit(-1);
		}
	}

	static void process_save() {
		try {
			System.out.println(">> saving .. ");
			PrintStream myOut = new PrintStream(path_result);
			myOut.println("time,cam_id,obj_id,u1,v1,u2,v2");

			for (int i = 0; i < action.frame_count; i++) {
				for (int j = 0; j < 2; j++) {
					ImgNode.ImgLine tmp = action.img_nodes[i][j].lines;
					while (tmp != null) {
						myOut.printf("%.4f,", action.img_nodes[i][j].time);
						myOut.printf("%d,-1", action.img_nodes[i][j].cam_id);
						int x1 = (int) (tmp.p1[0] * img_scale + 0.5f);
						int y1 = (int) (tmp.p1[1] * img_scale + 0.5f);
						int x2 = (int) (tmp.p2[0] * img_scale + 0.5f);
						int y2 = (int) (tmp.p2[1] * img_scale + 0.5f);
						myOut.printf(",%d,%d,%d,%d", x1, y1, x2, y2);
						myOut.println();
						tmp = tmp.next;
					}
				}
			}
			myOut.close();
			System.out.println(">> done .. ");
		} catch (FileNotFoundException e) {
			e.printStackTrace();
			System.err.println(">> save failed .. ");
		}
	}

	static void process_clean() {
		for (int i = 0; i < action.frame_count; i++) {
			for (int j = 0; j < 2; j++) {
				action.img_nodes[i][j].lines = null;
			}
		}
		System.out.println(">> all lines cleaned .. ");
	}

	static void process_load() {
		try {
			File file = new File(path_result);
			Scanner fr = new Scanner(file);
			fr.nextLine();

			process_clean();
			System.out.println(">> loading .. ");

			int idx_count = action.frame_count * 2;
			int idx_save, tmp_idx = -1;
			while (fr.hasNext()) {
				String line = fr.nextLine();
				String[] row = line.split(",");

				double img_id = Double.parseDouble(row[0]);
				int cam_id = Integer.parseInt(row[1]);
				int[] p1 = new int[2];
				p1[0] = (int) (0.5f + Integer.parseInt(row[3]) / img_scale);
				p1[1] = (int) (0.5f + Integer.parseInt(row[4]) / img_scale);
				int[] p2 = new int[2];
				p2[0] = (int) (0.5f + Integer.parseInt(row[5]) / img_scale);
				p2[1] = (int) (0.5f + Integer.parseInt(row[6]) / img_scale);

				while (true) {
					idx_save = tmp_idx;
					tmp_idx = (tmp_idx + 1) % idx_count;
					int i = tmp_idx / 2;
					int j = tmp_idx % 2;

					if (action.img_nodes[i][j].time > img_id + 1e-8) continue;
					if (action.img_nodes[i][j].time < img_id - 1e-8) continue;
					if (action.img_nodes[i][j].cam_id != cam_id) continue;

					action.img_nodes[i][j].add_line(p1, p2);
					tmp_idx = idx_save;
					break;
				}
			}
			fr.close();
			System.out.println(">> done .. ");
		} catch (FileNotFoundException ignored) {
			System.err.println(">> load failed .. ");
		}
	}

	private Main() {
		process_init();

		setLocation(600, 120);
		setSize(global_w, global_h + 22);
		setTitle("Manual Line Detection");
		setDefaultCloseOperation(EXIT_ON_CLOSE);

		MyJPanel panel = new MyJPanel();
		panel.setBackground(Color.BLACK);

		Mouse mouse = new Mouse();
		panel.addMouseListener(mouse);
		panel.addMouseMotionListener(mouse);

		Timer timer = new Timer(30, panel);
		timer.start();

		addKeyListener(new Keyboard());
		getContentPane().add(panel);
		setResizable(false);
		setVisible(true);

	}

	public static void main(String[] args) {
		new Main();
	}

}
