import java.awt.*;

public class MyObject {
    final float center_X = 0.5f * Main.board_width;
    final float center_Y = 0.5f * Main.board_height;
    final int point_size = 6;
    final int point_size2 = point_size * 2;
    final double NUM_ERR = 1e-9;

    final double R = 4.0;
    final double V = 1.0;
    final double K = 4.2;

    final double dt = 0.1;
    final double Vdt = V * dt;
    final double wdt = K * Vdt / R;

    final double rate = 0.9 * center_Y / R;

    // (dis, angle)
    double[] A = {0, 0};
    double[] B = {R, Math.PI};
    // final double r = Math.max(0.0, 1 - Math.PI / K) * R; // fastest
    final double r = R / K; // most safe

    final int R2 = (int) Math.round(R * 2 * rate);
    final int r2 = (int) Math.round(r * 2 * rate);


    final int idx_len = 100;
    int[][] points;
    int p_idx = 0;


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
        if (Ai[0] > r) {
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
        points = new int[idx_len][2];
        for (int i = 0; i < idx_len; i++) {
            points[i][0] = Math.round(center_X);
            points[i][1] = Math.round(center_Y);
        }
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
            points = new int[idx_len][2];
            points[0][0] = (int) Math.round(center_X + A[0] * Math.cos(A[1]) * rate);
            points[0][1] = (int) Math.round(center_Y - A[0] * Math.sin(A[1]) * rate);
            for (int i = 1; i < idx_len; i++) {
                points[i][0] = points[0][0];
                points[i][1] = points[0][1];
            }
            p_idx = 0;
        }
    }

    public void draw(Graphics2D g) {
        points[p_idx][0] = (int) Math.round(center_X + A[0] * Math.cos(A[1]) * rate);
        points[p_idx][1] = (int) Math.round(center_Y - A[0] * Math.sin(A[1]) * rate);
        p_idx = (p_idx + 1) % idx_len;
        g.setStroke(new BasicStroke(1.0f));
        g.setColor(new Color(180, 180, 30));
        for (int i = (p_idx + 2) % idx_len; i != p_idx; i = (i + 1) % idx_len) {
            int j = (i + idx_len - 1) % idx_len;
            g.drawLine(points[i][0], points[i][1], points[j][0], points[j][1]);
        }

        int[] pointA = func(A);
        int[] pointB = func(B);

        g.setColor(new Color(10, 150, 30));
        g.drawLine(pointA[0] + point_size, pointA[1] + point_size, pointB[0] + point_size, pointB[1] + point_size);

        g.setStroke(new BasicStroke(1.8f));
        g.setColor(new Color(100, 100, 100));
        g.drawOval((int) Math.round(center_X - R * rate), (int) Math.round(center_Y - R * rate), R2, R2);
        g.drawOval((int) Math.round(center_X - r * rate), (int) Math.round(center_Y - r * rate), r2, r2);

        g.setColor(new Color(40, 130, 250));
        g.fillOval(pointA[0], pointA[1], point_size2, point_size2);
        g.setColor(new Color(210, 10, 30));
        g.fillOval(pointB[0], pointB[1], point_size2, point_size2);

    }
}
