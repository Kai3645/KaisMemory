import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;

class Mouse implements MouseListener, MouseMotionListener {
	private static final int mouse_offset = Main.edge + 7;

	public void mouseClicked(MouseEvent me) {

	}

	public void mousePressed(MouseEvent me) {
		switch (me.getButton()) {
			case 1: {
				int x = me.getX() - mouse_offset;
				int y = me.getY() - mouse_offset;
				Main.action.add_point(x, y);
				break;
			}
			case 3: {
				Main.action.del_point();
				break;
			}
			case 4: {
				Main.action.frame_down();
				break;
			}
			case 5: {
				Main.action.frame_up();
				break;
			}
			default: {
				System.out.println(">> no action .. ");
			}
		}
	}

	public void mouseEntered(MouseEvent me) {

	}

	public void mouseExited(MouseEvent me) {

	}

	public void mouseReleased(MouseEvent me) {

	}

	public void mouseMoved(MouseEvent me) {
		Main.action.mouse_pos[0] = me.getX() - mouse_offset;
		Main.action.mouse_pos[1] = me.getY() - mouse_offset;
	}

	public void mouseDragged(MouseEvent me) {

	}
}
