from copy import copy
from typing import List, Optional, Dict, Any

from enginelib.claim_focus import ClaimFocus
from enginelib.claim_line_focus import ClaimLineFocus
from fhir.resources.claim import Claim
from schema.insight_engine_request import InsightEngineRequest
from schema.insight_engine_response import InsightEngineResponse, Insight

from enginelib.decor.traversal import TreeTraversal
from enginelib.decor.registry import Registry
from enginelib.decor.tree import Tree


class Policy:
    def __init__(self, request: InsightEngineRequest, historical_claims: List[Claim],
                 decision_tree: Tree, data: Optional[Dict[str, Any]] = None):
        self.cue = ClaimFocus(claim=request.claim, request=request)
        self.request = request
        self.historical_claims = [
            ClaimFocus(claim=claim, request=InsightEngineRequest.construct(claim=claim))
            for claim in historical_claims
        ]
        self.decision_tree = copy(decision_tree)
        self.data: Dict[str, Any] = data or dict()

    def evaluate(self) -> InsightEngineResponse:
        """Evaluates the policy for each claim line in self.request.claim.

        Returns:
            a response with the response.insights containing the list of insights
        """
        self.decision_tree.assemble()
        response = InsightEngineResponse()
        response.insights = [
            self._assess(clue)
            for clue in self.cue.lines
        ]
        return response

    def _assess(self, clue: ClaimLineFocus) -> Insight:
        """Assess one claim line according to the decision tree of the policy.

        Args:
            clue: claim line to assess.

        Returns:
            an insight for the given claim line.
        """
        registry = Registry(cue=self.cue, clue=clue, ocs=self.historical_claims, data=copy(self.data))
        simple_insight = TreeTraversal(self.decision_tree, registry).execute()
        return Insight(id=self.request.claim.id, type=simple_insight.insight_type,
                       description=simple_insight.text, claim_line_sequence_num=clue.sequence)
