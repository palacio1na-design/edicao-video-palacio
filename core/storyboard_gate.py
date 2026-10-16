#!/usr/bin/env python3
"""
PALÁCIO VÍDEOS 3.0 — STORYBOARD APPROVAL GATE (FASE 6)
Controle de Aprovação Humana (Human-in-the-Loop) Obrigatório.

REGRA ABSOLUTA:
Nenhuma renderização final pode começar sem a aprovação explícita do plano de cenas.
O sistema persiste o estado em 'storyboard_approval.json' e valida cada cena individualmente.
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, List, Optional


class StoryboardApprovalGate:
    """
    Gerencia o Gate Humano de Aprovação do Storyboard e Plano de Cenas.
    """

    def __init__(self, work_dir: str = "/Users/palacio.pro/.gemini/antigravity/scratch/motion_editor"):
        self.work_dir = work_dir
        self.plan_path = os.path.join(work_dir, "storyboard_plan.json")
        self.approval_path = os.path.join(work_dir, "storyboard_approval.json")
        os.makedirs(work_dir, exist_ok=True)

    def load_plan(self) -> Dict[str, Any]:
        """Carrega o plano de cenas gerado pelo SemanticSpeechEnricher."""
        if not os.path.exists(self.plan_path):
            raise FileNotFoundError(f"Plano de cenas não encontrado em {self.plan_path}. Execute o Semantic Enricher primeiro.")
        with open(self.plan_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_approval_state(self) -> Dict[str, Any]:
        """Carrega ou inicializa o estado de aprovação."""
        if os.path.exists(self.approval_path):
            with open(self.approval_path, "r", encoding="utf-8") as f:
                return json.load(f)

        # Se não existe, cria o estado inicial baseado no plano
        plan = self.load_plan()
        approval_state = {
            "version": "3.0.0",
            "video_path": plan.get("video_path", ""),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "is_fully_approved": False,
            "scenes": {
                s["scene_id"]: {
                    "speech_text": s["speech_text"],
                    "motion_type": s["motion_type"],
                    "status": "pending",  # 'approved', 'rejected', 'modified', 'pending'
                    "user_notes": ""
                }
                for s in plan.get("scenes", [])
            }
        }
        self.save_approval_state(approval_state)
        return approval_state

    def save_approval_state(self, state: Dict[str, Any]):
        """Salva o estado persistente de aprovação."""
        state["updated_at"] = datetime.now().isoformat()
        with open(self.approval_path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def approve_all(self, operator: str = "Marcelo Palácio") -> Dict[str, Any]:
        """Aprova todas as cenas de uma vez."""
        state = self.load_approval_state()
        for s_id in state["scenes"]:
            state["scenes"][s_id]["status"] = "approved"
            state["scenes"][s_id]["approved_by"] = operator
            state["scenes"][s_id]["approved_at"] = datetime.now().isoformat()
        state["is_fully_approved"] = True
        self.save_approval_state(state)
        return state

    def approve_scene(self, scene_id: str, operator: str = "Marcelo Palácio") -> Dict[str, Any]:
        """Aprova uma cena específica."""
        state = self.load_approval_state()
        if scene_id not in state["scenes"]:
            raise ValueError(f"Cena '{scene_id}' não existe no plano.")
        state["scenes"][scene_id]["status"] = "approved"
        state["scenes"][scene_id]["approved_by"] = operator
        state["scenes"][scene_id]["approved_at"] = datetime.now().isoformat()

        # Verifica se todas foram aprovadas
        all_appr = all(s["status"] == "approved" for s in state["scenes"].values())
        state["is_fully_approved"] = all_appr
        self.save_approval_state(state)
        return state

    def reject_scene(self, scene_id: str, reason: str = "") -> Dict[str, Any]:
        """Rejeita a animação de uma cena (o vídeo correrá em câmera original sem motion graphics)."""
        state = self.load_approval_state()
        if scene_id not in state["scenes"]:
            raise ValueError(f"Cena '{scene_id}' não existe no plano.")
        state["scenes"][scene_id]["status"] = "rejected"
        state["scenes"][scene_id]["motion_type"] = "none"
        state["scenes"][scene_id]["user_notes"] = f"Rejeitada: {reason}" if reason else "Rejeitada pelo usuário"
        state["is_fully_approved"] = False
        self.save_approval_state(state)
        return state

    def modify_scene(self, scene_id: str, new_motion_type: str, notes: str = "") -> Dict[str, Any]:
        """Modifica a animação de uma cena mantendo as demais intactas."""
        state = self.load_approval_state()
        if scene_id not in state["scenes"]:
            raise ValueError(f"Cena '{scene_id}' não existe no plano.")
        state["scenes"][scene_id]["status"] = "modified"
        state["scenes"][scene_id]["motion_type"] = new_motion_type
        state["scenes"][scene_id]["user_notes"] = notes
        state["is_fully_approved"] = False
        self.save_approval_state(state)
        return state

    def verify_can_render(self) -> Tuple[bool, str]:
        """
        Garante que nenhuma renderização aconteça sem aprovação humana expressa.
        Retorna (pode_renderizar, mensagem).
        """
        state = self.load_approval_state()
        pending = [s_id for s_id, s in state["scenes"].items() if s["status"] == "pending"]
        if pending:
            return False, f"BLOQUEIO DO GATE HUMANO: Existem {len(pending)} cena(s) pendente(s) de aprovação ({', '.join(pending)}). Use 'approve_all' ou aprove cena por cena antes de renderizar."

        # Se pelo menos uma cena foi aprovada ou modificada (e nenhuma pendente)
        can_proceed = any(s["status"] in ["approved", "modified", "rejected"] for s in state["scenes"].values())
        if not can_proceed:
            return False, "BLOQUEIO DO GATE HUMANO: Nenhuma cena aprovada para renderização."

        return True, "APROVAÇÃO VÁLIDA: Todas as decisões foram registradas pelo operador humano."

    def format_terminal_storyboard(self) -> str:
        """Formata o storyboard em formato textual limpo para visualização no terminal."""
        plan = self.load_plan()
        state = self.load_approval_state()

        lines = [
            "=" * 80,
            "PALÁCIO VÍDEOS 3.0 — STORYBOARD INTELIGENTE & GATE DE APROVAÇÃO HUMANA",
            "=" * 80,
            f"Vídeo Fonte: {os.path.basename(plan.get('video_path', ''))}",
            f"Total de Cenas: {len(plan.get('scenes', []))} | Status Geral: {'APROVADO' if state.get('is_fully_approved') else 'AGUARDANDO APROVAÇÃO'}",
            "-" * 80,
        ]

        for s in plan.get("scenes", []):
            s_id = s["scene_id"]
            appr = state["scenes"].get(s_id, {})
            status_icon = "✓ APROVADA" if appr.get("status") == "approved" else ("✗ REJEITADA" if appr.get("status") == "rejected" else "⏳ PENDENTE")

            lines.append(f"[{s_id.upper()}] {s['start_sec']}s -> {s['end_sec']}s ({s['duration_frames']} frames) | Status: {status_icon}")
            lines.append(f"  Fala: \"{s['speech_text']}\"")
            lines.append(f"  Significado: {s['meaning']}")
            lines.append(f"  Animação: {s['motion_type']} (Transição: {s['transition']})")
            lines.append(f"  Posicionamento: {s['layout_position'].get('anchor')} | Prioridade: {s['priority']}/5")
            lines.append(f"  Justificativa: {s['justification']}")
            if appr.get("user_notes"):
                lines.append(f"  Notas do Operador: {appr.get('user_notes')}")
            lines.append("-" * 80)

        lines.append("Comandos de Aprovação disponíveis:")
        lines.append("  • Aprovar Tudo:   python3 cli.py motion-approve <video> --all")
        lines.append("  • Aprovar Cena:   python3 cli.py motion-approve <video> --scene cena_01")
        lines.append("  • Rejeitar Cena:  python3 cli.py motion-reject  <video> --scene cena_02")
        lines.append("=" * 80)
        return "\n".join(lines)
