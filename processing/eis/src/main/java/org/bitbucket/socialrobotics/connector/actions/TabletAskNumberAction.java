package org.bitbucket.socialrobotics.connector.actions;

import java.util.List;

import eis.iilang.Identifier;
import eis.iilang.Numeral;
import eis.iilang.Parameter;

public class TabletAskNumberAction extends RobotAction {
	public final static String NAME = "askNumber";

	/**
	 * @param parameters A list of 1 numeral and 1 identifier: the number of digits
	 *                   that is accepted and the question that is to be displayed
	 *                   to the user.
	 */
	public TabletAskNumberAction(final List<Parameter> parameters) {
		super(parameters);
	}

	@Override
	public boolean isValid() {
		return (getParameters().size() == 2) && (getParameters().get(0) instanceof Numeral)
				&& (getParameters().get(1) instanceof Identifier);
	}

	@Override
	public String getTopic() {
		return "tablet_input_numbers";
	}

	@Override
	public String getData() {
		return (int) ((Numeral) getParameters().get(0)).getValue() + ";"
				+ ((Identifier) getParameters().get(1)).getValue();
	}
}
