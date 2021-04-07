import java.awt.*;

public class MyObject {
    final float center_X = 0.5f * Main.board_width;
    final float center_Y = 0.5f * Main.board_height;
    final float point_size = 6.5f;
    final int point_size2 = (int) point_size * 2;
    final double NUM_ERR = 1e-10;

    final double R = 5.0;
    final double V = 1.0;
    final double K = 4.5;

    final double rate = 0.95 * center_Y / R;

    // (dis, angle)
    double[] A = {0, 0};
    double[] B = {R, Math.PI};
    //    final double r = Math.max(0.0, 1 - Math.PI / K) * R; // fastest
    final double r = R / K; // most safe

    final int R2 = (int) Math.round(R * 2 * rate);
    final int r2 = (int) Math.round(r * 2 * rate);

    final double dt = 0.005;
    final double Vdt = V * dt;
    final double wdt = K * Vdt / R;

    double unwrap_angle(double a, double ref) {
        double pi2 = Math.PI * 2;
        double diff = a - ref;
        double fix = (int) (Math.abs(diff) / pi2 + 0.5) * pi2;
        if (diff > 0) return a - fix;
        return a + fix;
    }

    double[] fA(double[] Ai, double[] Bi) {
        if (Ai[0] <= 0) return new double[]{Vdt, unwrap_angle(Bi[1] - Math.PI, 0)};
        if (Math.abs(unwrap_angle(Bi[1] - Ai[1], 0)) < NUM_ERR) {
            Ai[0] -= Vdt;
            return Ai;
        }
        if (Ai[0] >= r) {
            Ai[0] += Vdt;
            return Ai;
        }
        double angle = unwrap_angle(Bi[1] - Math.PI, Ai[1]) - Ai[1];
        double v_ = Math.abs(angle / dt * Ai[0]);
        if (v_ > V) {
            Ai[0] -= Vdt;
            return Ai;
        }
        double vr = Math.sqrt(V * V - v_ * v_);
        Ai[0] += vr * dt;
        Ai[1] += angle;
        return Ai;
    }

    double[] fB(double[] Bi, double[] Ai) {
        if (Ai[0] == 0) return Bi;
        double angle = unwrap_angle(Ai[1] - Bi[1], 0);
        if (Math.abs(angle) < wdt) {
            Bi[1] += angle;
            return Bi;
        }
        if (Math.abs(angle) + wdt > Math.PI) {
            Bi[1] += wdt;
            return Bi;
        }
        if (angle < 0) Bi[1] -= wdt;
        else Bi[1] += wdt;
        return Bi;
    }

    int[] func(double[] X) {
        int xi = (int) Math.round(center_X + X[0] * Math.cos(X[1]) * rate - point_size);
        int yi = (int) Math.round(center_Y - X[0] * Math.sin(X[1]) * rate - point_size);
        return new int[]{xi, yi};
    }

    public MyObject() {
        System.out.println(">> initiating .. ");
//        if (K * r > R) System.err.println("bad, case");
        System.out.println(">> initiated");
    }

    public void save() {
        System.out.println(">> saving .. ");

        System.out.println(">> saved .. ");
    }

    public void update() {
        if (A[0] < R) {
            A = fA(A, B);
            B = fB(B, A);
        } else {
            A[0] = Math.random() * r;
            A[1] = Math.random() * Math.PI * 2;
        }
    }

    public void draw(Graphics2D g) {
        int[] pointA = func(A);
        int[] pointB = func(B);
        g.setStroke(new BasicStroke(1.3f));
        g.setColor(new Color(100, 100, 100));
        g.drawOval((int) Math.round(center_X - R * rate), (int) Math.round(center_Y - R * rate), R2, R2);
        g.drawOval((int) Math.round(center_X - r * rate), (int) Math.round(center_Y - r * rate), r2, r2);

        g.setColor(new Color(200, 10, 30));
        g.fillOval(pointA[0], pointA[1], point_size2, point_size2);
        g.setColor(new Color(20, 130, 220));
        g.fillOval(pointB[0], pointB[1], point_size2, point_size2);

    }
}
