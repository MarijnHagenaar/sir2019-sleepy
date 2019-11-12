package org.bitbucket.socialrobotics.connector.actions;

import java.util.List;

import eis.iilang.Identifier;
import eis.iilang.Parameter;
import eis.iilang.ParameterList;

public class StartListeningAction extends RobotAction {
	public final static String NAME = "startListening";

	/**
	 * @param parameters A list of 1 identifier indicating the context (optional)
	 */
	public StartListeningAction(final List<Parameter> parameters) {
		super(parameters);
	}

	@Override
	public boolean isValid() {
		return (getParameters().isEmpty())
				|| (getParameters().size() == 1 && getParameters().get(0) instanceof Identifier)
				|| (getParameters().size() == 2 && getParameters().get(0) instanceof Identifier
						&& getParameters().get(1) instanceof ParameterList);
	}

	public String getContext() {
		return getParameters().isEmpty() ? "" : ((Identifier) getParameters().get(0)).toProlog();
	}

	public String getHints() {
		if (getParameters().size() == 2) {
			final StringBuilder data = new StringBuilder();
			for (final Parameter param : ((ParameterList) getParameters().get(1))) {
				data.append(((Identifier) param).getValue()).append('|');
			}
			return data.toString();
		} else {
			return "";
		}
	}

	@Override
	public String getTopic() {
		return "action_audio";
	}

	@Override
	public String getData() {
		return "start listening";
	}
}
