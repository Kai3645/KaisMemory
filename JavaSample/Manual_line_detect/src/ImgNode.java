import javax.imageio.ImageIO;
import java.awt.*;
import java.io.File;
import java.io.IOException;

class ImgNode {
	double time;
	int cam_id;
	private String path;
	ImgLine lines = null;

	ImgNode(double time, int cam_id, String path) {
		this.time = time;
		this.cam_id = cam_id;
		this.path = path;
	}

	static class ImgLine {
		ImgLine next = null;
		int[] p1;
		int[] p2;

		ImgLine(int[] p1, int[] p2) {
			this.p1 = new int[]{p1[0], p1[1]};
			this.p2 = new int[]{p2[0], p2[1]};
		}

//		ImgLine(int x1, int y1, int x2, int y2) {
//			this.p1 = new int[]{x1, y1};
//			this.p2 = new int[]{x2, y2};
//		}

		private String str() {
			String tmp_str = "";
			tmp_str += String.format("(( %d, %d ), ", this.p1[0], this.p1[1]);
			tmp_str += String.format("( %d, %d ))\n", this.p2[0], this.p2[1]);
			return tmp_str;
		}

	}

	void add_line(int[] p1, int[] p2) {
		ImgLine new_line = new ImgLine(p1, p2);
		if (this.lines == null) {
			this.lines = new_line;
			return;
		}
		ImgLine tmp = this.lines;
		while (tmp.next != null) tmp = tmp.next;
		tmp.next = new_line;
	}

	int[] pop_line() {
		if (this.lines == null) return null;
		if (this.lines.next == null) {
			int[] p1 = this.lines.p1;
			this.lines = null;
			return p1;
		}
		ImgLine tmp = this.lines;
		while (tmp.next.next != null) tmp = tmp.next;
		int[] p1 = tmp.next.p1;
		tmp.next = null;
		return p1;
	}

	private int line_len() {
		int length = 0;
		ImgLine tmp = this.lines;
		while (tmp != null) {
			tmp = tmp.next;
			length++;
		}
		return length;
	}

	void print() {
		System.out.printf("time = %.4f, ", this.time);
		System.out.printf("cam_id = %d, ", this.cam_id);
		System.out.printf("lines = %d ", this.line_len());
	}

	void draw(Graphics2D g2d, int x, int y) {
		try {
			Image img = ImageIO.read(new File(this.path));
			g2d.drawImage(img, x, y, null);

			int h = img.getHeight(null);
			int w = img.getWidth(null);

//			g2d.setColor(new Color(0, 0, 0, 100));
//			g2d.fillRect(0, 0, w, (int) (h * 0.47 + 0.5));
//			g2d.setColor(new Color(0, 0, 0, 70));
//			g2d.fillRect(0, 0, w, (int) (h * 0.57 + 0.5));
//			g2d.setColor(new Color(0, 0, 0, 30));
//			g2d.fillRect(0, 0, w, (int) (h * 0.73 + 0.5));

//			g2d.setStroke(new BasicStroke(1));
//			g2d.setColor(new Color(255, 20, 147, 140));
//			g2d.drawLine(0, (int) (h * 0.47 + 0.5), w, (int) (h * 0.47 + 0.5));
//			g2d.setColor(new Color(65, 105, 225, 180));
//			g2d.drawLine(0, (int) (h * 0.57 + 0.5), w, (int) (h * 0.57 + 0.5));
//			g2d.setColor(new Color(50, 205, 50, 180));
//			g2d.drawLine(0, (int) (h * 0.73 + 0.5), w, (int) (h * 0.73 + 0.5));


			g2d.setStroke(new BasicStroke(2.333f));
			ImgLine tmp = this.lines;
			while (tmp != null) {
				g2d.setColor(new Color(220, 20, 60, 200));
				g2d.drawLine(tmp.p1[0], tmp.p1[1], tmp.p2[0], tmp.p2[1]);
				g2d.setColor(new Color(255, 140, 0, 200));
				g2d.drawOval(tmp.p1[0] - 7, tmp.p1[1] - 7, 14, 14);
				g2d.drawOval(tmp.p2[0] - 7, tmp.p2[1] - 7, 14, 14);

				tmp = tmp.next;
			}
		} catch (IOException ignored) {
			System.err.println("can not read image " + this.path);
		}
	}


}

