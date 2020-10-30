import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

class Keyboard extends KeyAdapter {
    public void keyPressed(KeyEvent e) {
        switch (e.getKeyCode()) {
            case KeyEvent.VK_ESCAPE -> {
                System.out.println(">> key -> esc");
                Main.action.escape();
            }
            case KeyEvent.VK_UP -> {
                System.out.println(">> key -> up");
                Main.action.direction(0);
            }
            case KeyEvent.VK_DOWN -> {
                System.out.println(">> key -> down");
                Main.action.direction(1);
            }
            case KeyEvent.VK_LEFT -> {
                System.out.println(">> key -> left");
                Main.action.direction(2);
            }
            case KeyEvent.VK_RIGHT -> {
                System.out.println(">> key -> right");
                Main.action.direction(3);
            }
            default -> {
                System.out.println(">> unknown key .. ");
                return;
            }
        }
        Main.panel.repaint();
    }

    public void keyReleased(KeyEvent e) {

    }

    public void keyTyped(KeyEvent e) {

    }

}
