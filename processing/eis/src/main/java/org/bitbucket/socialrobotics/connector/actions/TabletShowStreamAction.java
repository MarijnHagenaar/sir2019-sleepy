package org.bitbucket.socialrobotics.connector.actions;

public class TabletShowStreamAction extends RobotAction {
	public final static String NAME = "showStream";

	public TabletShowStreamAction() {
		super(null);
	}

	@Override
	public boolean isValid() {
		return true;
	}

	@Override
	public String getTopic() {
		return "tablet_stream";
	}

	@Override
	public String getData() {
		return "";
	}
}
