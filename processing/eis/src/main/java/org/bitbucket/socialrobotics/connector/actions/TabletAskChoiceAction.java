package org.bitbucket.socialrobotics.connector.actions;

import java.util.List;

import eis.iilang.Identifier;
import eis.iilang.Parameter;
import eis.iilang.ParameterList;

public class TabletAskChoiceAction extends RobotAction {
	public final static String NAME = "askChoice";

	/**
	 * @param parameters A list of an identifier and a parameterlist: the question
	 *                   and a list of answers.
	 */
	public TabletAskChoiceAction(final List<Parameter> parameters) {
		super(parameters);
	}

	@Override
	public boolean isValid() {
		return (getParameters().size() == 2) && (getParameters().get(0) instanceof Identifier)
				&& (getParameters().get(1) instanceof ParameterList);
	}

	@Override
	public String getTopic() {
		return "tablet_input_multiple";
	}

	@Override
	public String getData() {
		final StringBuilder data = new StringBuilder();
		data.append(((Identifier) getParameters().get(0)).getValue());
		for (final Parameter param : ((ParameterList) getParameters().get(1))) {
			data.append(';').append(((Identifier) param).getValue());
		}
		return data.toString();
	}
}
