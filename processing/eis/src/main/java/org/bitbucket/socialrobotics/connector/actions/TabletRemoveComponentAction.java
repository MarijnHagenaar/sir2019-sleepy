package org.bitbucket.socialrobotics.connector.actions;

import java.util.List;

import eis.iilang.Identifier;
import eis.iilang.Parameter;

public class TabletRemoveComponentAction extends RobotAction {
	public final static String NAME = "removeTabletComponent";

	/**
	 * @param parameters A list of 1 identifier: the name of the component. This
	 *                   actually is not actually sent to Redis, but the data is
	 *                   queued up until the next 'real' tablet action is called,
	 *                   because the tablet needs all components to be set at once.
	 */
	public TabletRemoveComponentAction(final List<Parameter> parameters) {
		super(parameters);
	}

	@Override
	public boolean isValid() {
		return (getParameters().size() == 1) && (getParameters().get(0) instanceof Identifier);
	}

	@Override
	public String getTopic() {
		return null;
	}

	@Override
	public String getData() {
		return ((Identifier) getParameters().get(0)).getValue();
	}
}
