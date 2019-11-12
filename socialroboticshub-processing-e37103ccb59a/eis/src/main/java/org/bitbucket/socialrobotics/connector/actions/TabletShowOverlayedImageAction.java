package org.bitbucket.socialrobotics.connector.actions;

import java.util.List;

import eis.iilang.Identifier;
import eis.iilang.Parameter;

public class TabletShowOverlayedImageAction extends RobotAction {
	public final static String NAME = "showOverlayedImage";

	/**
	 * @param parameters A list of 2 identifiers: an image URL for the main image
	 *                   and an image URL for the overlay
	 */
	public TabletShowOverlayedImageAction(final List<Parameter> parameters) {
		super(parameters);
	}

	@Override
	public boolean isValid() {
		return (getParameters().size() == 2) && (getParameters().get(0) instanceof Identifier)
				&& (getParameters().get(1) instanceof Identifier);
	}

	@Override
	public String getTopic() {
		return "tablet_overlay";
	}

	@Override
	public String getData() {
		return ((Identifier) getParameters().get(0)).getValue() + ";"
				+ ((Identifier) getParameters().get(1)).getValue();
	}
}
