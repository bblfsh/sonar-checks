public class MyServlet extends HttpServlet {
  public void doGet(HttpServletRequest req, HttpServletResponse res) throws ServletException, IOException {
    if (userIsAuthorized(req)) {
      updatePrices(req);
    }
  }

  public static void main(String[] args) { // Noncompliant
    updatePrices(req);
  }
}
