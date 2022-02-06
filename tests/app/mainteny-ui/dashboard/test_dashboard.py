"""DASHBOARD TEST MODULE """


def test_dashboard(_user_login, frontend):
    """ Verify the pending orders in Dashboard."""
    expected_pending_orders = '55'
    frontend.py.wait(use_py=True).sleep(3)
    actual__pending_orders = frontend.dashboard_page.pending_orders.text().strip()
    assert expected_pending_orders == actual__pending_orders, "Pending orders didn't match with expectation."

