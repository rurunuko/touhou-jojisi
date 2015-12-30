# -*- coding: utf-8 -*-
# This file is part of Civ IV Gameplay Enhancements
# Copyright Civ IV Gameplay Enhancements 2006-2008

#重要: このファイルはUTF-8エンコードで保存してください。
import sys

# reminder preset message
# プリセット・メッセージ設定
# ユーザ各自で設定してください。
reminderPreset = [
	u"ユーザプリセット1",
	u"ユーザプリセット2",
	u"ユーザプリセット3",
	u"プリセットテスト",
	]

# city placement marker text
# 都市建設予定地マーカー文字列
cityPlacementMakerPreset = u"予定地: "

# Unit Placements marker text
# ユニット自動配置 集合地点マーカー文字列
unitPlacementsMakerPreset = u"U.P.: "

# Auto Order All not active units at begin turn
# ターン開始時に活動していないユニットに対し命令を出す
# 生産したユニットに対し命令を出す
# 優先順位はユニットクラス(AutoOrderUnitClass)、戦闘タイプ(AutoOrderCombatType)の順。
# 可能な命令:
#	"NONE":			何もしない
#	"SLEEP":		スリープ
#	"INTERCEPT":	迎撃
EnableAutoOrder = False
# 戦争時にキャンセルする
DisableAutoOrderAtWar = True
# 戦闘タイプによる命令指定
# タイプはXML\Units\CIV4UnitCombatInfos.xmlで定義されているものの"UNITCOMBAT_"以下を指定。
# "OtherType"は戦闘タイプが指定されていない全てのユニットに対する命令となる。
AutoOrderCombatType = {
	"OtherType":	"SLEEP",
	"RECON":		"SLEEP",
	"ARCHER":		"SLEEP",
	"MOUNTED":		"SLEEP",
	"MELEE":		"SLEEP",
	"SIEGE":		"SLEEP",
	"GUN":			"SLEEP",
	"ARMOR":		"SLEEP",
	"HELICOPTER":	"SLEEP",
	"NAVAL":		"SLEEP",
	"AIR":			"SLEEP",
}
# ユニットクラスによる命令指定
# タイプはXML\Units\CIV4UnitInfos.xmlで定義されているものの"UNITCLASS_"以下を指定。
AutoOrderUnitClass = {
	"WORKER":		"NONE",
	"FIGHTER":		"INTERCEPT",
	"JET_FIGHTER":	"INTERCEPT",
}
# 上記AutoOrderCombatType, AutoOrderUnitClassの設定は"WORKER"(労働者、固有ユニット含む)以外のユニットをスリープする
# また、"FIGHTER"、"JET_FIGHTER"を迎撃にする。


# Vistaで一部機能を使用不可にする
# 無効にする場合、ifの2行をコメントアウト
vistaCheck = True
if (sys.getwindowsversion()[0] > 5):
	vistaCheck = False
