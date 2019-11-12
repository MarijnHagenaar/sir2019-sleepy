package org.bitbucket.socialrobotics.connector;

import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

import org.bitbucket.socialrobotics.connector.actions.CloseAction;
import org.bitbucket.socialrobotics.connector.actions.RobotAction;
import org.bitbucket.socialrobotics.connector.actions.TabletAddComponentAction;
import org.bitbucket.socialrobotics.connector.actions.TabletRemoveComponentAction;

import redis.clients.jedis.Jedis;

class RedisProducerRunner extends RedisRunner {
	private final BlockingQueue<RobotAction> actionQueue;
	private final List<String> tabletComponents;
	private boolean tabletNeedsUpdate = false;

	public RedisProducerRunner(final CBSRenvironment parent, final String server) {
		super(parent, server);
		this.actionQueue = new LinkedBlockingQueue<>();
		this.tabletComponents = new LinkedList<>();
	}

	@Override
	public void run() {
		final Jedis redis = getRedis();
		// process the action queue into outgoing messages
		while (isRunning()) {
			try {
				System.out.println("Waiting for action...");
				final RobotAction next = this.actionQueue.take();
				if (next instanceof CloseAction) {
					super.shutdown();
				} else if (next instanceof TabletAddComponentAction) {
					this.tabletComponents.add(next.getData());
					this.tabletNeedsUpdate = true;
				} else if (next instanceof TabletRemoveComponentAction) {
					removeTabletComponent(next.getData());
					this.tabletNeedsUpdate = true;
				} else {
					System.out.println("Got " + next.getData() + " on " + next.getTopic());
					if (this.tabletNeedsUpdate && next.getClass().getSimpleName().startsWith("Tablet")) {
						System.out.println("Updating tablet components...");
						redis.publish("tablet_config", getTabletComponents());
						this.tabletNeedsUpdate = false;
					}
					redis.publish(next.getTopic(), next.getData());
				}
			} catch (final Exception e) {
				if (isRunning()) {
					e.printStackTrace(); // FIXME
				}
			}
		}
	}

	private void removeTabletComponent(final String name) {
		final Iterator<String> iterator = this.tabletComponents.iterator();
		while (iterator.hasNext()) {
			if (iterator.next().startsWith(name)) {
				iterator.remove();
				break;
			}
		}
	}

	private String getTabletComponents() {
		final StringBuilder components = new StringBuilder();
		for (final String component : this.tabletComponents) {
			components.append(component).append(';');
		}
		return components.toString();
	}

	public void queueAction(final RobotAction action) {
		this.actionQueue.add(action);
	}

	@Override
	public void shutdown() {
		queueAction(new CloseAction());
	}
}