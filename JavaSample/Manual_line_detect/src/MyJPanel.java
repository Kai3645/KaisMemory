import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;

class MyJPanel extends JPanel implements ActionListener {
	private static BufferedImage bufImg;
	private static Graphics2D g2d;

	MyJPanel() {
		bufImg = new BufferedImage(Main.board_w, Main.board_h, BufferedImage.TYPE_INT_ARGB);
		g2d = (Graphics2D) bufImg.getGraphics();
		g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
		g2d.setRenderingHint(RenderingHints.KEY_INTERPOLATION, RenderingHints.VALUE_INTERPOLATION_BICUBIC);
	}

	public void paint(Graphics g) {
		super.paint(g2d);

		Main.action.draw(g2d);

		// draw edge
		g2d.setColor(new Color(238, 130, 238,150));
		g2d.setStroke(new BasicStroke(1));
		g2d.drawRect(0, 0, Main.board_w - 1, Main.board_h - 1);

		g.drawImage(bufImg, Main.edge, Main.edge, null);
	}

	public void actionPerformed(ActionEvent e) {
		if (Main.action.finish_flag) {
			setVisible(false);
			Main.process_save();
			System.out.println(">> process finished .. ");
			System.exit(0);
		}

		repaint();
	}

}
