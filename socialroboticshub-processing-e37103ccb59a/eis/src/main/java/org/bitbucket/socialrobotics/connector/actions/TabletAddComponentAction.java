package org.bitbucket.socialrobotics.connector.actions;

import java.util.List;

import eis.iilang.Identifier;
import eis.iilang.Parameter;
import eis.iilang.ParameterList;

public class TabletAddComponentAction extends RobotAction {
	public final static String NAME = "addTabletComponent";

	/**
	 * @param parameters A list of 2 identifiers and 1 optional parameterlist: the
	 *                   name of the component, its position (top/bottom), and
	 *                   optional arguments (key=value). This actually is not
	 *                   actually sent to Redis, but the data is queued up until the
	 *                   next 'real' tablet action is called, because the tablet
	 *                   needs all components to be set at once.
	 */
	public TabletAddComponentAction(final List<Parameter> parameters) {
		super(parameters);
	}

	@Override
	public boolean isValid() {
		boolean valid = (getParameters().size() == 2) || (getParameters().size() == 3);
		valid &= getParameters().get(0) instanceof Identifier;
		valid &= getParameters().get(1) instanceof Identifier;
		if (getParameters().size() == 3) {
			valid &= getParameters().get(2) instanceof ParameterList;
		}
		return valid;
	}

	@Override
	public String getTopic() {
		return null;
	}

	@Override
	public String getData() {
		final StringBuilder data = new StringBuilder();
		data.append(((Identifier) getParameters().get(0)).getValue());
		data.append(',').append(((Identifier) getParameters().get(1)).getValue());
		if (getParameters().size() == 3) {
			for (final Parameter param : ((ParameterList) getParameters().get(2))) {
				data.append(',').append(((Identifier) param).getValue());
			}
		}
		return data.toString();
	}
}
