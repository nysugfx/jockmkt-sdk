

type WebsocketMessage =
  | {
      action: 'authenticate';
      authentication: {
        type: 'token';
        token: string;
      };
    }
  | {
      action: 'subscribe' | 'unsubscribe';
      subscription: {
        type: 'event';
        event_id: string;
      };
    }
  | {
      action: 'subscribe' | 'unsubscribe';
      subscription: {
        type: 'event_activity';
        event_id: string;
      };
    }
  | {
      action: 'subscribe';
      subscription: {
        type: 'account';
      };
    }
  | {
      action: 'subscribe';
      subscription: {
        type: 'notification';
      };
    }
  | {
      action: 'subscribe' | 'unsubscribe';
      subscription: {
        type: 'games';
        league: string;
      };
    };

type AuthenticationResponse = {
  object: 'authentication';
  status: 'success' | 'error';
};

type ErrorResponse = {
  object: 'error';
  error: string;
};

type SubscriptionResponse =
  | {
      object: 'subscription';
      status: 'subscribed' | 'unsubscribed';
      type: 'event' | 'event_activity';
      event_id: string;
    }
  | {
      object: 'subscription';
      status: 'subscribed' | 'unsubscribed';
      type: 'account';
    }
  | {
      object: 'subscription';
      status: 'subscribed' | 'unsubscribed';
      type: 'notification';
    }
  | {
      object: 'subscription';
      status: 'subscribed' | 'unsubscribed';
      type: 'games';
      league: string;
    };

type Operation = 'created' | 'updated' | 'deleted';

type DataResponse =
  | {
      subscription: 'event';
      event_id: string;
      object: 'tradeable';
      operation: Operation;
      tradeable: Tradeable;
    }
  | {
      subscription: 'games';
      object: 'game';
      operation: Operation;
      game: Game;
    }
  | {
      subscription: 'event';
      event_id: string;
      object: 'event';
      operation: Operation;
      event: Event;
    }
  | {
      subscription: 'account';
      object: 'entry';
      operation: Operation;
      entry: Entry;
    }
  | {
      subscription: 'account';
      object: 'balance';
      operation: Operation;
      balance: Balance;
    }
  | {
      subscription: 'account';
      object: 'position';
      operation: Operation;
      position: Position;
    }
  | {
      subscription: 'account';
      object: 'order';
      operation: Operation;
      order: Order;
    }
  | {
      subscription: 'account';
      object: 'payout';
      operation: Operation;
      payout: Payout;
    }
  | {
      subscription: 'notification';
      object: 'notification';
      operation: Operation;
      notification: Notification;
    }
  | {
      subscription: 'event_activity';
      event_id: string;
      object: 'order';
      operation: Operation;
      order: PublicOrderActivity;
    }
  | {
      subscription: 'event_activity';
      event_id: string;
      object: 'trade';
      operation: Operation;
      trade: Trade;
    }
  | {
      subscription: 'event_activity';
      event_id: string;
      object: 'join';
      operation: Operation;
      join: Join;
    };

type WebsocketResponse = AuthenticationResponse | SubscriptionResponse | ErrorResponse | DataResponse;

class WebsocketProvider {
  private static instance: WebsocketProvider;
  private socket: WebSocket | undefined;
  private isAuthenticated = false;
  private status: 'disconnected' | 'connecting' | 'connected' = 'disconnected';

  private eventSubscription?: { event_id: string; created_at: Date };

  public static getInstance = () => {
    if (!WebsocketProvider.instance) {
      WebsocketProvider.instance = new WebsocketProvider();
      WebsocketProvider.instance.createConnection();
    }
    return WebsocketProvider.instance;
  };

  private setConnectionStatus = (status: 'disconnected' | 'connecting' | 'connected') => {
    this.status = status;
    store.dispatch(setWebsocketConnectionStatus(status));
  };

  public connect = () => {
    if (this.status !== 'connecting' && this.status !== 'connected') {
      this.createConnection();
    }
  };

  public disconnect = () => {
    if (this.socket) this.socket.close();
  };

  private createConnection = async () => {
    if (this.socket) this.socket.close();

    this.setConnectionStatus('connecting');
    this.socket = new WebSocket(
      `wss://${process.env.NEXT_PUBLIC_JMK_API_BASE_URL || 'stage.api.jockmkt.net'}/streaming`
    );

    /**
     * On socket connection, perform the authentication
     */
    this.socket.onopen = async () => {
      this.setConnectionStatus('connected');

      let token = undefined;

      while (token == null) {
        token = getToken();
        await new Promise(r => setTimeout(r, 1000));
      }

      const authentication = {
        action: 'authenticate',
        authentication: {
          type: 'token',
          token: getToken()
        }
      };

      /* send our authentication request */
      if (this.socket) this.socket.send(JSON.stringify(authentication));
    };

    this.socket.onerror = () => {
      if (this.socket) this.socket.close();
    };

    this.socket.onclose = () => {
      this.setConnectionStatus('disconnected');

      setTimeout(() => {
        const authenticated = selectAuthed(store.getState());
        if (authenticated && this.status === 'disconnected') this.createConnection();
      }, 5000);
    };

    this.socket.onmessage = (data: any) => {
      const response = JSON.parse(data.data) as WebsocketResponse;

      // close on error
      if (response.object === 'error') {
        this.socket?.close();
        return;
      }

      switch (response.object) {
        case 'authentication':
          {
            if (response.status === 'success') {
              this.isAuthenticated = true;
              store.dispatch(setWebsocketAuthenticationStatus(true));

              const accountSubscription: WebsocketMessage = {
                action: 'subscribe',
                subscription: {
                  type: 'account'
                }
              };

              const notificationSubscription: WebsocketMessage = {
                action: 'subscribe',
                subscription: {
                  type: 'notification'
                }
              };

              /* send our authentication request */
              if (this.socket) this.socket.send(JSON.stringify(accountSubscription));
              if (this.socket) this.socket.send(JSON.stringify(notificationSubscription));

              /* if there is an event focus, we subscribe to it */
              const focusEventId = selectActiveEvent(store.getState());
              const activeLeague = selectActiveLeague(store.getState());
              if (focusEventId || activeLeague) {
                this.emitEventSubscriptionRequests({
                  league: activeLeague ?? undefined,
                  event_id: focusEventId ?? undefined
                });
              }
            } else {
              this.socket?.close();
            }
          }
          break;
        case 'subscription':
          {
            switch (response.type) {
              case 'event':
                {
                  const subscription = response.status === 'subscribed' ? response.event_id : undefined;
                  store.dispatch(setWebsocketEventSubscription(subscription));
                }
                break;
              case 'event_activity':
                {
                  const subscription = response.status === 'subscribed' ? response.event_id : undefined;
                  store.dispatch(setWebsocketEventActivitySubscription(subscription));
                }
                break;
              case 'account':
              case 'notification':
                {
                  // TODO - console.warn('DEV NOTE: webhooks-subscription-account - Not Implemented');
                }
                break;
              case 'games':
                {
                  const subscription = response.status === 'subscribed' ? response.league : undefined;
                  store.dispatch(setWebsocketGameSubscription(subscription));
                }
                break;
              default: {
                console.log(response);
              }
            }
          }
          break;
        case 'tradeable':
          {
            store.dispatch(upsertTradeable(response.tradeable));
          }
          break;
        case 'game':
          {
            store.dispatch(upsertGame(response.game));
          }
          break;
        case 'event':
          {
            store.dispatch(upsertEvent(response.event));
          }
          break;
        case 'entry':
          {
            switch (response.operation) {
              case 'updated': {
                store.dispatch(upsertEntry(response.entry));
                break;
              }
              default: {
                store.dispatch(upsertEntry(response.entry));
              }
            }
          }
          break;
        case 'balance':
          {
            store.dispatch(upsertBalance(response.balance));
          }
          break;
        case 'position':
          {
            store.dispatch(upsertPosition(response.position));
          }
          break;
        case 'order':
          {
            switch (response.subscription) {
              case 'account': {
                store.dispatch(upsertOrder(response.order));
                break;
              }
              case 'event_activity': {
                store.dispatch(upsertEventActivity({ event_id: response.event_id, activity: response.order }));
                break;
              }
            }
          }
          break;
        case 'join': {
          store.dispatch(upsertEventActivity({ event_id: response.event_id, activity: response.join }));
          break;
        }
        case 'payout': {
          store.dispatch(upsertPayout(response.payout));
          break;
        }
        case 'notification': {
          switch (response.operation) {
            case 'created': {
              store.dispatch(upsertNotificationFromSocket(response.notification));
              break;
            }
            case 'updated': {
              store.dispatch(upsertNotification(response.notification));
              break;
            }
          }
          break;
        }
        default: {
          console.log(response);
        }
      }

      // if (data.data === 'heartbeat') {
      //   console.log(data.data)
      //   return
      // }

      // console.log(`Roundtrip time: ${Date.now() - data.data} ms`)
      // console.log(data)
      // setTimeout(function timeout() {
      // ws.send('heartbeat')
      // }, 15000)
    };
  };

  public updateFocusEvent = async ({ event_id, league }: { event_id?: string; league?: string }) => {
    const socket = selectSocket(store.getState());
    if (socket.isAuthenticated && (event_id || league)) this.emitEventSubscriptionRequests({ event_id, league });
    else if (socket.isAuthenticated) this.emitEventUnsubscriptionSubscriptionRequests();
  };

  private emitEventSubscriptionRequests = async ({ event_id, league }: { event_id?: string; league?: string }) => {
    if (this.socket && this.status === 'connected') {
      // console.log(`Subscribing to event & event activity streams for ${event_id}`);

      if (event_id) {
        const event_subscription: WebsocketMessage = {
          action: 'subscribe',
          subscription: {
            type: 'event',
            event_id
          }
        };
        const event_activity_subscription: WebsocketMessage = {
          action: 'subscribe',
          subscription: {
            type: 'event_activity',
            event_id
          }
        };

        this.socket.send(JSON.stringify(event_subscription));
        this.socket.send(JSON.stringify(event_activity_subscription));
      }

      if (league) {
        const game_subscription: WebsocketMessage = {
          action: 'subscribe',
          subscription: {
            type: 'games',
            league
          }
        };
        this.socket.send(JSON.stringify(game_subscription));
      }
    }
  };

  private emitEventUnsubscriptionSubscriptionRequests = async () => {
    const socket = selectSocket(store.getState());
    const eventSubscription = socket.subscriptions.event?.id;
    const eventActivitySubscription = socket.subscriptions.event_activity?.id;
    const gameSubscription = socket.subscriptions.game?.id;

    if (eventSubscription) {
      // console.log(`Unsubscribing to event stream for ${eventSubscription}`);

      const event_subscription: WebsocketMessage = {
        action: 'unsubscribe',
        subscription: {
          type: 'event',
          event_id: eventSubscription
        }
      };
      if (this.socket) this.socket.send(JSON.stringify(event_subscription));
    }

    if (gameSubscription) {
      // console.log(`Unsubscribing to event stream for ${eventSubscription}`);

      const game_subscription: WebsocketMessage = {
        action: 'unsubscribe',
        subscription: {
          type: 'games',
          league: gameSubscription
        }
      };
      if (this.socket) this.socket.send(JSON.stringify(game_subscription));
    }

    if (eventActivitySubscription) {
      // console.log(`Unsubscribing to event activity stream for ${eventActivitySubscription}`);

      const event_subscription: WebsocketMessage = {
        action: 'unsubscribe',
        subscription: {
          type: 'event_activity',
          event_id: eventActivitySubscription
        }
      };
      if (this.socket) this.socket.send(JSON.stringify(event_subscription));
    }
  };
}

/**
 * Schedules actions with { meta: { delay: N } } to be delayed by N milliseconds.
 * Makes `dispatch` return a function to cancel the timeout in this case.
 */
export const webhookMiddleware: Middleware = () => next => action => {
  const init = once(() => {
    WebsocketProvider.getInstance();
  });

  init();

  // if (!action.type.startsWith('jockmkt') && !action.type.startsWith('__rtkq')) console.log(action.type);

  if (action.type === 'focus/setEvent') {
    WebsocketProvider.getInstance().updateFocusEvent({ event_id: action.payload });
  } else if (action.type === 'focus/setEventMetadata') {
    WebsocketProvider.getInstance().updateFocusEvent({ league: action.payload.league });
  } else if (action.type === 'auth/setAuth') {
    WebsocketProvider.getInstance().connect();
  } else if (action.type === 'auth/setNoAuth') {
    WebsocketProvider.getInstance().disconnect();
  }

  return next(action);
};
