import javax.swing.*;
import java.awt.*;
import java.awt.image.BufferedImage;

class MyJPanel extends JPanel {
    MyJPanel() { }

    public void paint(Graphics g) {
        super.paint(g);

        BufferedImage bufImg = new BufferedImage(Main.board_width, Main.board_height, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2d = (Graphics2D) bufImg.getGraphics();
        g2d.setStroke(new BasicStroke(2.5f));
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2d.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL, RenderingHints.VALUE_STROKE_DEFAULT);

        Main.action.paint(g2d);
        // draw edge
        g.setColor(new Color(238, 130, 238));
        g.drawRect(Main.board_edge - 1, Main.board_edge - 1, Main.board_width + 1, Main.board_height + 1);

        g.drawImage(bufImg, Main.board_edge, Main.board_edge, null);

//        int cx = Main.action.mouse_pos[0] + Main.board_edge;
//        int cy = Main.action.mouse_pos[1] + Main.board_edge;
//        g.setColor(new Color(0, 200, 255, 200));
//
//        g.drawLine(cx, 0, cx, Main.global_height);
//        g.drawLine(0, cy, Main.global_width, cy);
    }

}
