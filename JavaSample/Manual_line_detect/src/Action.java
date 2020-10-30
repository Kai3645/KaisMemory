import java.awt.*;

class Action {
	ImgNode[][] img_nodes;
	int frame_count;
	int current_cam_idx = 0;
	int current_img_idx = 0;

	int[] mouse_pos = new int[2];
	int[] p1 = new int[2];
	private int[] p2 = new int[2];

	boolean is_first = true;
	boolean finish_flag = false;

	private static final double len_short = 80;
	private static final double len_long = 300;

	private double line_len(double dx, double dy) {
		return Math.sqrt(dx * dx + dy * dy);
	}

	void add_point(int x, int y) {
		System.out.printf(">> add point (%d, %d)\n", x, y);
		if (is_first) {
			is_first = false;
			p1[0] = x;
			p1[1] = y;
			return;
		}
		int dx = x - p1[0];
		int dy = y - p1[1];
		double length = line_len(dx, dy);
		if (length < len_short) {
			System.out.printf(">> too short %.1f \n", length);
			return;
		}
		if (length > len_long) {
			System.out.printf(">> too long %.1f \n", length);
			x = (int) (0.5 + dx * len_long / length) + p1[0];
			y = (int) (0.5 + dy * len_long / length) + p1[1];
			length = line_len(x - p1[0], y - p1[1]);
			System.out.printf(">> fix point (%d, %d)\n", x, y);
		}
		is_first = true;
		p2[0] = x;
		p2[1] = y;
		img_nodes[current_img_idx][current_cam_idx].add_line(p1, p2);
		System.out.printf(">> new line %.1f \n", length);
	}

	void del_point() {
		System.out.println(">> push back .. ");
		if (is_first) {
			int[] tmp_p1 = img_nodes[current_img_idx][current_cam_idx].pop_line();
			if (tmp_p1 != null) {
				is_first = false;
				p1[0] = tmp_p1[0];
				p1[1] = tmp_p1[1];
			}
		} else {
			is_first = true;
		}
	}

	void current_info() {
		System.out.printf(">> current frame %d, ", current_img_idx);
		img_nodes[current_img_idx][current_cam_idx].print();
		System.out.println();
	}

	void frame_up() {
		System.out.println(">> swap up .. ");
		if (current_img_idx < 1) {
			System.out.println(">> enddle .. ");
			return;
		}
		current_img_idx -= 1;
		current_info();
		is_first = true;
	}

	void frame_down() {
		System.out.println(">> swap down .. ");
		if (current_img_idx + 1 >= frame_count) {
			System.out.println(">> enddle .. ");
			return;
		}
		current_img_idx += 1;
		current_info();
		is_first = true;
	}

	void frame_left() {
		System.out.println(">> swap left .. ");
		if (current_cam_idx == 0) {
			System.out.println(">> enddle .. ");
			return;
		}
		current_cam_idx -= 1;
		current_info();
		is_first = true;
	}

	void frame_right() {
		System.out.println(">> swap right .. ");
		if (current_cam_idx == 1) {
			System.out.println(">> enddle .. ");
			return;
		}
		current_cam_idx += 1;
		current_info();
		is_first = true;
	}

	void frame_clean() {
		img_nodes[current_img_idx][current_cam_idx].lines = null;
		is_first = true;
		System.out.println(">> frame lines cleaned .. ");
	}

	void draw(Graphics2D g2d) {
		img_nodes[current_img_idx][current_cam_idx].draw(g2d, 0, 0);
		g2d.setStroke(new BasicStroke(1.6f));

		if (!is_first) {
			g2d.setColor(new Color(200, 0, 0, 200));
			g2d.drawLine(p1[0], p1[1], mouse_pos[0], mouse_pos[1]);
			g2d.setColor(Color.magenta);
			g2d.drawLine(p1[0], p1[1] + 9, p1[0], p1[1] - 9);
			g2d.drawLine(p1[0] + 9, p1[1], p1[0] - 9, p1[1]);
		}

		g2d.setColor(Color.red);
		g2d.drawLine(mouse_pos[0], mouse_pos[1] + 9, mouse_pos[0], mouse_pos[1] - 9);
		g2d.drawLine(mouse_pos[0] + 9, mouse_pos[1], mouse_pos[0] - 9, mouse_pos[1]);
	}

}
