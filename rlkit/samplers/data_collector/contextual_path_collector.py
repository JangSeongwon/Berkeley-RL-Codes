from functools import partial

from rlkit.envs.contextual import ContextualEnv
from rlkit.policies.base import Policy
from rlkit.samplers.data_collector import MdpPathCollector
from rlkit.samplers.rollout_functions import contextual_rollout


class ContextualPathCollector(MdpPathCollector):
    def __init__(
            self,
            env: ContextualEnv,
            policy: Policy,
            max_num_epoch_paths_saved=None,
            observation_keys=('observation',),
            context_keys_for_policy='context',
            render=False,
            render_kwargs=None,
            **kwargs
    ):
        rollout_fn = partial(
            contextual_rollout,
            context_keys_for_policy=context_keys_for_policy,
            observation_keys=observation_keys,
        )
        super().__init__(
            env, policy,
            max_num_epoch_paths_saved=max_num_epoch_paths_saved,
            render=render,
            render_kwargs=render_kwargs,
            rollout_fn=rollout_fn,
            **kwargs
        )
        self._observation_keys = observation_keys
        self._context_keys_for_policy = context_keys_for_policy

    def get_snapshot(self):
        snapshot = super().get_snapshot()
        snapshot.update(
            observation_keys=self._observation_keys,
            context_keys_for_policy=self._context_keys_for_policy,
        )
        return snapshot
