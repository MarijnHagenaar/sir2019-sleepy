package org.bitbucket.socialrobotics.connector.actions;

import java.util.List;

import eis.iilang.Identifier;
import eis.iilang.Numeral;
import eis.iilang.Parameter;

public class TabletAskRatingAction extends RobotAction {
	public final static String NAME = "askRating";

	/**
	 * @param parameters A list of 1 numeral and 1 identifier: the scale of the
	 *                   rating and the according question that is to be displayed
	 *                   to the user.
	 */
	public TabletAskRatingAction(final List<Parameter> parameters) {
		super(parameters);
	}

	@Override
	public boolean isValid() {
		return (getParameters().size() == 2) && (getParameters().get(0) instanceof Numeral)
				&& (getParameters().get(1) instanceof Identifier);
	}

	@Override
	public String getTopic() {
		return "tablet_question_rate";
	}

	@Override
	public String getData() {
		return (int) ((Numeral) getParameters().get(0)).getValue() + ";"
				+ ((Identifier) getParameters().get(1)).getValue();
	}
}
