import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;

class Mouse implements MouseListener, MouseMotionListener {
    private static void set_mouse_pos(MouseEvent e) {
        Main.action.mouse_pos[0] = e.getX() - Main.board_edge;
        Main.action.mouse_pos[1] = e.getY() - Main.board_edge;
    }

    public void mouseClicked(MouseEvent e) {
    }

    public void mousePressed(MouseEvent e) {
        set_mouse_pos(e);
        switch (e.getButton()) {
            case 1 -> {
                System.out.println(">> mouse -> left");
                Main.action.mouse_left();
            }
            case 3 -> {
                System.out.println(">> mouse -> right");
                Main.action.mouse_right();
            }
            case 4 -> {
                System.out.println(">> mouse -> ex 1");
                Main.action.mouse_ex1();
            }
            case 5 -> {
                System.out.println(">> mouse -> ex 2");
                Main.action.mouse_ex2();
            }
        }
        Main.panel.repaint();

    }

    public void mouseEntered(MouseEvent e) {

    }

    public void mouseExited(MouseEvent e) {

    }

    public void mouseReleased(MouseEvent e) {

    }

    public void mouseMoved(MouseEvent e) {
        set_mouse_pos(e);
        Main.action.mouse_moved();
        Main.panel.repaint();
    }

    public void mouseDragged(MouseEvent e) {

    }
}
