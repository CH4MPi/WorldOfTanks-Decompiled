# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/impl/gen/resources/strings_entries/ingame_gui.py
from gui.impl.gen_utils import DynAccessor

class IngameGui(DynAccessor):
    __slots__ = ()

    class aim(DynAccessor):
        __slots__ = ()
        zoom = 1596

    class attackReason(DynAccessor):
        __slots__ = ()
        artilleryProtection = 1631
        artillery_sector = 1632
        bombers = 1633

    class battleEndWarning(DynAccessor):
        __slots__ = ()
        text = 1601

    class battleMessenger(DynAccessor):
        __slots__ = ()

        class toxic(DynAccessor):
            __slots__ = ()

            class blackList(DynAccessor):
                __slots__ = ()

                class ADD_IN_BLACKLIST(DynAccessor):
                    __slots__ = ()
                    body = 1607
                    header = 1606

                class CANT_ADD_IN_BLACKLIST(DynAccessor):
                    __slots__ = ()
                    body = 1609
                    header = 1608

                class REMOVE_FROM_BLACKLIST(DynAccessor):
                    __slots__ = ()
                    body = 1611
                    header = 1610

    class battleProgress(DynAccessor):
        __slots__ = ()

        class hint(DynAccessor):
            __slots__ = ()
            description = 1640
            noBindingKey = 1659
            press = 1639

    class burnout(DynAccessor):
        __slots__ = ()

        class hint(DynAccessor):
            __slots__ = ()
            engineDamageWarning = 1662

    class chat_example(DynAccessor):
        __slots__ = ()
        attack = 1163
        attack_enemy = 1168
        attention_to_cell = 1167
        back_to_base = 1164
        follow_me = 1162

        class global_msg(DynAccessor):
            __slots__ = ()

            class atk(DynAccessor):
                __slots__ = ()
                focus_hq = 1150
                save_tanks = 1144
                time = 1145

            class c_def(DynAccessor):
                __slots__ = ()
                focus_hq = 1151
                save_tanks = 1142
                time = 1146

            class lane(DynAccessor):
                __slots__ = ()
                center = 1148
                east = 1149
                west = 1147

        help_me = 1160
        help_me_ex = 1161
        negative = 1166
        positive = 1165
        reloading_cassette = 1154
        reloading_gun = 1153
        reloading_ready = 1155
        reloading_ready_cassette = 1157
        reloading_unavailable = 1158
        spg_aim_area = 1169
        stop = 1159
        support_me_with_fire = 1152
        turn_back = 1156

    class chat_shortcuts(DynAccessor):
        __slots__ = ()
        attack = 1119
        attack_enemy = 1140
        attack_enemy_reloading = 1141
        attention_to_base_atk = 1129
        attention_to_base_def = 1130
        attention_to_cell = 1123
        attention_to_objective_atk = 1127
        attention_to_objective_def = 1128
        attention_to_position = 1126
        back_to_base = 1120
        follow_me = 1118

        class global_msg(DynAccessor):
            __slots__ = ()

            class atk(DynAccessor):
                __slots__ = ()
                focus_hq = 1138
                save_tanks = 1131
                time = 1133

            class c_def(DynAccessor):
                __slots__ = ()
                focus_hq = 1139
                save_tanks = 1132
                time = 1134

            class lane(DynAccessor):
                __slots__ = ()
                center = 1136
                east = 1137
                west = 1135

        help_me = 1116
        help_me_ex = 1117
        negative = 1122
        positive = 1121
        reloading_cassette = 1111
        reloading_gun = 1110
        reloading_ready = 1112
        reloading_ready_cassette = 1113
        reloading_unavailable = 1114
        spg_aim_area = 1124
        spg_aim_area_reloading = 1125
        stop = 1115
        support_me_with_fire = 1109
        turn_back = 1108

    class colorSettingsTipPanel(DynAccessor):
        __slots__ = ()
        btnLabel = 1641

    class consumables_panel(DynAccessor):
        __slots__ = ()

        class equipment(DynAccessor):
            __slots__ = ()
            cooldownSeconds = 1280

            class tooltip(DynAccessor):
                __slots__ = ()
                empty = 1279

    class countRibbons(DynAccessor):
        __slots__ = ()
        multiSeparator = 1541

    class cruise_ctrl(DynAccessor):
        __slots__ = ()
        speedMetric = 1278

    class damageIndicator(DynAccessor):
        __slots__ = ()
        multiplier = 1602

    class damageLog(DynAccessor):
        __slots__ = ()
        multiplier = 1565

        class shellType(DynAccessor):
            __slots__ = ()
            ARMOR_PIERCING = 1560
            ARMOR_PIERCING_CR = 1563
            ARMOR_PIERCING_HE = 1562
            HIGH_EXPLOSIVE = 1561
            HOLLOW_CHARGE = 1564

    class damage_panel(DynAccessor):
        __slots__ = ()

        class crew(DynAccessor):
            __slots__ = ()

            class commander(DynAccessor):
                __slots__ = ()
                destroyed = 1263
                normal = 1262

            class driver(DynAccessor):
                __slots__ = ()
                destroyed = 1265
                normal = 1264

            class gunner1(DynAccessor):
                __slots__ = ()
                destroyed = 1271
                normal = 1270

            class gunner2(DynAccessor):
                __slots__ = ()
                destroyed = 1273
                normal = 1272

            class loader1(DynAccessor):
                __slots__ = ()
                destroyed = 1275
                normal = 1274

            class loader2(DynAccessor):
                __slots__ = ()
                destroyed = 1277
                normal = 1276

            class radioman1(DynAccessor):
                __slots__ = ()
                destroyed = 1267
                normal = 1266

            class radioman2(DynAccessor):
                __slots__ = ()
                destroyed = 1269
                normal = 1268

        class devices(DynAccessor):
            __slots__ = ()

            class ammoBay(DynAccessor):
                __slots__ = ()
                critical = 1242
                destroyed = 1243
                normal = 1241

            class chassis(DynAccessor):
                __slots__ = ()
                critical = 1248
                destroyed = 1249
                normal = 1247

            class engine(DynAccessor):
                __slots__ = ()
                critical = 1236
                destroyed = 1237
                normal = 1235

            class fuelTank(DynAccessor):
                __slots__ = ()
                critical = 1257
                destroyed = 1258
                normal = 1256

            class gun(DynAccessor):
                __slots__ = ()
                critical = 1239
                destroyed = 1240
                normal = 1238

            class radio(DynAccessor):
                __slots__ = ()
                critical = 1254
                destroyed = 1255
                normal = 1253

            class surveyingDevice(DynAccessor):
                __slots__ = ()
                critical = 1260
                destroyed = 1261
                normal = 1259

            class track(DynAccessor):
                __slots__ = ()
                critical = 1245
                destroyed = 1246
                normal = 1244

            class turretRotator(DynAccessor):
                __slots__ = ()
                critical = 1233
                destroyed = 1234
                normal = 1232

            class wheel(DynAccessor):
                __slots__ = ()
                critical = 1251
                destroyed = 1252
                normal = 1250

    class devices(DynAccessor):
        __slots__ = ()
        ammo_bay = 1038
        chassis = 1046
        engine = 1037
        fuel_tank = 1039
        gun = 1043
        left_track = 1041
        radio = 1040
        right_track = 1042
        surveing_device = 1045
        turret_rotator = 1044
        wheel = 1047

    class distance(DynAccessor):
        __slots__ = ()
        meters = 1597

    class dynamicSquad(DynAccessor):
        __slots__ = ()

        class ally(DynAccessor):
            __slots__ = ()
            add = 1587
            disabled = 1589
            received = 1594
            wasSent = 1591

        class enemy(DynAccessor):
            __slots__ = ()
            add = 1588
            disabled = 1590
            received = 1595
            wasSent = 1592

        invite = 1593

    class efficiencyRibbons(DynAccessor):
        __slots__ = ()
        armor = 1542
        assistByAbility = 1627
        assistSpot = 1551
        assistTrack = 1550
        burn = 1546
        capture = 1543
        crits = 1552
        damage = 1544
        defence = 1547
        defenderBonus = 1626
        destructibleDamaged = 1623
        destructibleDestroyed = 1624
        destructiblesDefended = 1625
        enemySectorCaptured = 1622
        kill = 1548
        ram = 1545
        receivedBurn = 1556
        receivedCrits = 1554
        receivedDamage = 1555
        receivedRam = 1557
        receivedWorldCollision = 1558
        spotted = 1549
        stun = 1566
        vehicleRecovery = 1559
        worldCollision = 1553

    class epic_players_panel(DynAccessor):
        __slots__ = ()

        class state(DynAccessor):
            __slots__ = ()

            class hidden(DynAccessor):
                __slots__ = ()
                body = 1310
                header = 1309
                note = 1311

            class medium_player(DynAccessor):
                __slots__ = ()
                body = 1316
                header = 1315
                note = 1317

            class medium_tank(DynAccessor):
                __slots__ = ()
                body = 1319
                header = 1318
                note = 1320

            class short(DynAccessor):
                __slots__ = ()
                body = 1313
                header = 1312
                note = 1314

            class toggle(DynAccessor):
                __slots__ = ()
                body = 1322
                header = 1321
                note = 1323

    class flagNotification(DynAccessor):
        __slots__ = ()
        flagAbsorbed = 1583
        flagCaptured = 1580
        flagDelivered = 1582
        flagInbase = 1581

    class flags(DynAccessor):
        __slots__ = ()
        timer = 1540

    class fortConsumables(DynAccessor):
        __slots__ = ()

        class timer(DynAccessor):
            __slots__ = ()
            postfix = 1539

    class helpScreen(DynAccessor):
        __slots__ = ()

        class hint(DynAccessor):
            __slots__ = ()
            press = 1660

    class helpscreen(DynAccessor):
        __slots__ = ()

        class hint(DynAccessor):
            __slots__ = ()
            description = 1661

    class hitMarker(DynAccessor):
        __slots__ = ()
        blocked = 1567
        critical = 1569
        ricochet = 1568

    class marker(DynAccessor):
        __slots__ = ()
        meters = 1143

    class personalMissions(DynAccessor):
        __slots__ = ()

        class tip(DynAccessor):
            __slots__ = ()
            additionalHeader = 1536
            mainHeader = 1535

            class noQuests(DynAccessor):
                __slots__ = ()
                battleType = 1538
                vehicleType = 1537

    class player_errors(DynAccessor):
        __slots__ = ()

        class cant_move(DynAccessor):
            __slots__ = ()
            chassis_damaged = 1055
            crew_inactive = 1053
            engine_damaged = 1054

        class cant_shoot(DynAccessor):
            __slots__ = ()
            crew_inactive = 1057
            gun_damaged = 1059
            gun_locked = 1061
            gun_reload = 1060
            no_ammo = 1058
            vehicle_destroyed = 1056

        class cant_switch(DynAccessor):
            __slots__ = ()
            engine_destroyed = 1062

        class equipment(DynAccessor):
            __slots__ = ()
            alreadyActivated = 1063

            class extinguisher(DynAccessor):
                __slots__ = ()
                doesNotActivated = 1069

            isInCooldown = 1064

            class medkit(DynAccessor):
                __slots__ = ()
                allTankmenAreSafe = 1066
                tankmanIsSafe = 1065

            class order(DynAccessor):
                __slots__ = ()
                notReady = 1070

            class repairkit(DynAccessor):
                __slots__ = ()
                allDevicesAreNotDamaged = 1068
                deviceIsNotDamaged = 1067

    class player_messages(DynAccessor):
        __slots__ = ()
        ALLY_HIT = 1085
        COMBAT_EQUIPMENT_READY_ARTILLERY = 1436
        COMBAT_EQUIPMENT_READY_BOMBER = 1437
        COMBAT_EQUIPMENT_READY_INSPIRE = 1440
        COMBAT_EQUIPMENT_READY_RECON = 1438
        COMBAT_EQUIPMENT_READY_SMOKE = 1439
        COMBAT_EQUIPMENT_USED_ARTILLERY = 1441
        COMBAT_EQUIPMENT_USED_BOMBER = 1442
        COMBAT_EQUIPMENT_USED_INSPIRE = 1445
        COMBAT_EQUIPMENT_USED_RECON = 1443
        COMBAT_EQUIPMENT_USED_SMOKE = 1444
        DEATH_FROM_ARTILLERY_ALLY_ALLY = 1398
        DEATH_FROM_ARTILLERY_ALLY_ENEMY = 1399
        DEATH_FROM_ARTILLERY_ALLY_SUICIDE = 1395
        DEATH_FROM_ARTILLERY_ENEMY_ALLY = 1401
        DEATH_FROM_ARTILLERY_ENEMY_ENEMY = 1400
        DEATH_FROM_ARTILLERY_ENEMY_SUICIDE = 1394
        DEATH_FROM_ARTILLERY_PROTECTION_UNKNOWN_ALLY = 1405
        DEATH_FROM_ARTILLERY_PROTECTION_UNKNOWN_ENEMY = 1404
        DEATH_FROM_BOMBER_ALLY_SUICIDE = 1397
        DEATH_FROM_BOMBER_ENEMY_SUICIDE = 1396
        DEATH_FROM_DEATH_ZONE_ALLY_ALLY = 1493
        DEATH_FROM_DEATH_ZONE_ALLY_ENEMY = 1494
        DEATH_FROM_DEATH_ZONE_ALLY_SELF = 1492
        DEATH_FROM_DEATH_ZONE_ALLY_SUICIDE = 1491
        DEATH_FROM_DEATH_ZONE_ENEMY_ALLY = 1497
        DEATH_FROM_DEATH_ZONE_ENEMY_ENEMY = 1498
        DEATH_FROM_DEATH_ZONE_ENEMY_SELF = 1496
        DEATH_FROM_DEATH_ZONE_ENEMY_SUICIDE = 1495
        DEATH_FROM_DEATH_ZONE_SELF_ALLY = 1489
        DEATH_FROM_DEATH_ZONE_SELF_ENEMY = 1490
        DEATH_FROM_DEATH_ZONE_SELF_SUICIDE = 1488
        DEATH_FROM_DEVICE_EXPLOSION_AT_FIRE = 1417
        DEATH_FROM_DEVICE_EXPLOSION_AT_SHOT = 1415
        DEATH_FROM_DROWNING_ALLY_ALLY = 1430
        DEATH_FROM_DROWNING_ALLY_ENEMY = 1431
        DEATH_FROM_DROWNING_ALLY_SELF = 1429
        DEATH_FROM_DROWNING_ALLY_SUICIDE = 1428
        DEATH_FROM_DROWNING_ENEMY_ALLY = 1434
        DEATH_FROM_DROWNING_ENEMY_ENEMY = 1435
        DEATH_FROM_DROWNING_ENEMY_SELF = 1433
        DEATH_FROM_DROWNING_ENEMY_SUICIDE = 1432
        DEATH_FROM_DROWNING_SELF_ALLY = 1426
        DEATH_FROM_DROWNING_SELF_ENEMY = 1427
        DEATH_FROM_DROWNING_SELF_SUICIDE = 1425
        DEATH_FROM_GAS_ATTACK_ALLY_ALLY = 1502
        DEATH_FROM_GAS_ATTACK_ALLY_ENEMY = 1503
        DEATH_FROM_GAS_ATTACK_ALLY_SELF = 1501
        DEATH_FROM_GAS_ATTACK_ENEMY_ALLY = 1505
        DEATH_FROM_GAS_ATTACK_ENEMY_ENEMY = 1506
        DEATH_FROM_GAS_ATTACK_ENEMY_SELF = 1504
        DEATH_FROM_GAS_ATTACK_SELF_ALLY = 1499
        DEATH_FROM_GAS_ATTACK_SELF_ENEMY = 1500
        DEATH_FROM_INACTIVE_CREW = 1414
        DEATH_FROM_INACTIVE_CREW_AT_SHOT = 1412
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_ALLY_ALLY = 1474
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_ALLY_ENEMY = 1475
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_ALLY_SELF = 1473
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_ALLY_SUICIDE = 1472
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_ENEMY_ALLY = 1478
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_ENEMY_ENEMY = 1479
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_ENEMY_SELF = 1477
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_ENEMY_SUICIDE = 1476
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_SELF_ALLY = 1470
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_SELF_ENEMY = 1471
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_SELF_SUICIDE = 1469
        DEATH_FROM_OVERTURN_ALLY_ALLY = 1525
        DEATH_FROM_OVERTURN_ALLY_ENEMY = 1526
        DEATH_FROM_OVERTURN_ALLY_SELF = 1524
        DEATH_FROM_OVERTURN_ALLY_SUICIDE = 1523
        DEATH_FROM_OVERTURN_ENEMY_ALLY = 1529
        DEATH_FROM_OVERTURN_ENEMY_ENEMY = 1530
        DEATH_FROM_OVERTURN_ENEMY_SELF = 1528
        DEATH_FROM_OVERTURN_ENEMY_SUICIDE = 1527
        DEATH_FROM_OVERTURN_SELF_ALLY = 1521
        DEATH_FROM_OVERTURN_SELF_ENEMY = 1522
        DEATH_FROM_OVERTURN_SELF_SUICIDE = 1520
        DEATH_FROM_RAMMING_ALLY_ALLY = 1518
        DEATH_FROM_RAMMING_ALLY_ENEMY = 1519
        DEATH_FROM_RAMMING_ALLY_SELF = 1517
        DEATH_FROM_RAMMING_ALLY_SUICIDE = 1516
        DEATH_FROM_RAMMING_ENEMY_ALLY = 1533
        DEATH_FROM_RAMMING_ENEMY_ENEMY = 1534
        DEATH_FROM_RAMMING_ENEMY_SELF = 1532
        DEATH_FROM_RAMMING_ENEMY_SUICIDE = 1531
        DEATH_FROM_RAMMING_SELF_ALLY = 1514
        DEATH_FROM_RAMMING_SELF_ENEMY = 1515
        DEATH_FROM_RAMMING_SELF_SUICIDE = 1513
        DEATH_FROM_RECOVERY_ALLY_SUICIDE = 1403
        DEATH_FROM_RECOVERY_ENEMY_SUICIDE = 1402
        DEATH_FROM_SECTOR_BOMBERS_UNKNOWN_ALLY = 1409
        DEATH_FROM_SECTOR_BOMBERS_UNKNOWN_ENEMY = 1408
        DEATH_FROM_SECTOR_PROTECTION_UNKNOWN_ALLY = 1407
        DEATH_FROM_SECTOR_PROTECTION_UNKNOWN_ENEMY = 1406
        DEATH_FROM_SHOT_ALLY_ALLY = 1376
        DEATH_FROM_SHOT_ALLY_ALLY_ARTILLERY = 1377
        DEATH_FROM_SHOT_ALLY_ALLY_BOMBER = 1378
        DEATH_FROM_SHOT_ALLY_ENEMY = 1379
        DEATH_FROM_SHOT_ALLY_ENEMY_ARTILLERY = 1380
        DEATH_FROM_SHOT_ALLY_ENEMY_BOMBER = 1381
        DEATH_FROM_SHOT_ALLY_SUICIDE = 1382
        DEATH_FROM_SHOT_ALLY_SUICIDE_ARTILLERY = 1383
        DEATH_FROM_SHOT_ALLY_SUICIDE_BOMBER = 1384
        DEATH_FROM_SHOT_ENEMY_ALLY = 1388
        DEATH_FROM_SHOT_ENEMY_ALLY_ARTILLERY = 1389
        DEATH_FROM_SHOT_ENEMY_ALLY_BOMBER = 1390
        DEATH_FROM_SHOT_ENEMY_ENEMY = 1391
        DEATH_FROM_SHOT_ENEMY_ENEMY_ARTILLERY = 1392
        DEATH_FROM_SHOT_ENEMY_ENEMY_BOMBER = 1393
        DEATH_FROM_SHOT_ENEMY_SUICIDE = 1385
        DEATH_FROM_SHOT_ENEMY_SUICIDE_ARTILLERY = 1386
        DEATH_FROM_SHOT_ENEMY_SUICIDE_BOMBER = 1387
        DEATH_FROM_SHOT_SELF_ALLY = 1370
        DEATH_FROM_SHOT_SELF_ALLY_ARTILLERY = 1371
        DEATH_FROM_SHOT_SELF_ALLY_BOMBER = 1372
        DEATH_FROM_SHOT_SELF_ENEMY = 1373
        DEATH_FROM_SHOT_SELF_ENEMY_ARTILLERY = 1374
        DEATH_FROM_SHOT_SELF_ENEMY_BOMBER = 1375
        DEATH_FROM_WORLD_COLLISION_ALLY_ALLY = 1457
        DEATH_FROM_WORLD_COLLISION_ALLY_ENEMY = 1458
        DEATH_FROM_WORLD_COLLISION_ALLY_SELF = 1456
        DEATH_FROM_WORLD_COLLISION_ALLY_SUICIDE = 1455
        DEATH_FROM_WORLD_COLLISION_ENEMY_ALLY = 1461
        DEATH_FROM_WORLD_COLLISION_ENEMY_ENEMY = 1462
        DEATH_FROM_WORLD_COLLISION_ENEMY_SELF = 1460
        DEATH_FROM_WORLD_COLLISION_ENEMY_SUICIDE = 1459
        DEATH_FROM_WORLD_COLLISION_SELF_ALLY = 1453
        DEATH_FROM_WORLD_COLLISION_SELF_ENEMY = 1454
        DEATH_FROM_WORLD_COLLISION_SELF_SUICIDE = 1452
        DESTRUCTIBLE_DESTROYED_ALLY = 1613
        DESTRUCTIBLE_DESTROYED_ENEMY = 1614
        DESTRUCTIBLE_DESTROYED_SELF = 1612
        DEVICE_CRITICAL_AT_FIRE = 1075
        DEVICE_CRITICAL_AT_SHOT = 1071
        DEVICE_DESTROYED_AT_FIRE = 1080
        DEVICE_DESTROYED_AT_SHOT = 1072
        DEVICE_REPAIRED = 1084
        DEVICE_REPAIRED_TO_CRITICAL = 1081
        DEVICE_STARTED_FIRE_AT_SHOT = 1073
        ENGINE_CRITICAL_AT_BURNOUT = 1078
        ENGINE_CRITICAL_AT_UNLIMITED_RPM = 1076
        ENGINE_DESTROYED_AT_BURNOUT = 1079
        ENGINE_DESTROYED_AT_UNLIMITED_RPM = 1077
        FIRE_STOPPED = 1082
        TANKMAN_HIT_AT_SHOT = 1074
        TANKMAN_RESTORED = 1083
        allied_team_name = 1093
        ally_base_captured_by_notification = 1089
        ally_base_captured_notification = 1086
        base_capture_blocked = 1092
        base_captured_by_notification = 1091
        base_captured_notification = 1088
        enemy_base_captured_by_notification = 1090
        enemy_base_captured_notification = 1087
        enemy_team_name = 1094
        loader_intuition_was_used = 1107

        class postmortem_caption(DynAccessor):
            __slots__ = ()
            other = 1097
            self = 1096

        postmortem_caption_ = 1095
        postmortem_userNoHasAmmo = 1098
        replayControlsHelp1 = 1104
        replayControlsHelp2 = 1105
        replayControlsHelp3 = 1106
        replayFreeCameraActivated = 1100
        replayPaused = 1103
        replaySavedCameraActivated = 1101
        replaySpeedChange = 1102
        tank_in_fire = 1099

    class players_panel(DynAccessor):
        __slots__ = ()

        class state(DynAccessor):
            __slots__ = ()

            class large(DynAccessor):
                __slots__ = ()
                body = 1302
                header = 1301
                note = 1303

            class medium(DynAccessor):
                __slots__ = ()
                body = 1296
                header = 1295
                note = 1297

            class medium2(DynAccessor):
                __slots__ = ()
                body = 1299
                header = 1298
                note = 1300

            class none(DynAccessor):
                __slots__ = ()
                body = 1290
                header = 1289
                note = 1291

            class short(DynAccessor):
                __slots__ = ()
                body = 1293
                header = 1292
                note = 1294

        unknown_clan = 1308
        unknown_frags = 1306
        unknown_name = 1304
        unknown_vehicle = 1305
        unknown_vehicleState = 1307

    class postmortem(DynAccessor):
        __slots__ = ()

        class tips(DynAccessor):
            __slots__ = ()

            class exitHangar(DynAccessor):
                __slots__ = ()
                label = 1287
                text = 1288

            class observerMode(DynAccessor):
                __slots__ = ()
                label = 1285
                text = 1286

    class postmortem_messages(DynAccessor):
        __slots__ = ()
        DEATH_FROM_DEATH_ZONE_ALLY_SELF = 1485
        DEATH_FROM_DEATH_ZONE_ENEMY_SELF = 1483
        DEATH_FROM_DEATH_ZONE_SELF_SUICIDE = 1481
        DEATH_FROM_DEVICE_EXPLOSION_AT_FIRE = 1418
        DEATH_FROM_DEVICE_EXPLOSION_AT_SHOT = 1416
        DEATH_FROM_DROWNING_ALLY_SELF = 1424
        DEATH_FROM_DROWNING_ENEMY_SELF = 1422
        DEATH_FROM_DROWNING_SELF_SUICIDE = 1420
        DEATH_FROM_FIRE = 1411
        DEATH_FROM_INACTIVE_CREW_AT_SHOT = 1413
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_ALLY_SELF = 1468
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_ENEMY_SELF = 1466
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_SELF_SUICIDE = 1464
        DEATH_FROM_OVERTURN_ALLY_SELF = 1369
        DEATH_FROM_OVERTURN_ENEMY_SELF = 1368
        DEATH_FROM_OVERTURN_SELF_SUICIDE = 1367
        DEATH_FROM_RAMMING_ALLY_SELF = 1512
        DEATH_FROM_RAMMING_ENEMY_SELF = 1510
        DEATH_FROM_RAMMING_SELF_SUICIDE = 1508
        DEATH_FROM_SHOT = 1361
        DEATH_FROM_SHOT_ARTILLERY = 1365
        DEATH_FROM_SHOT_BOMBER = 1366
        DEATH_FROM_WORLD_COLLISION_ALLY_SELF = 1451
        DEATH_FROM_WORLD_COLLISION_ENEMY_SELF = 1449
        DEATH_FROM_WORLD_COLLISION_SELF_SUICIDE = 1447
        DEATH_UNKNOWN = 1362

    class recovery(DynAccessor):
        __slots__ = ()
        cooldown = 1630
        hint1 = 1628
        hint2 = 1629

    class repairPoint(DynAccessor):
        __slots__ = ()
        title = 1599
        unavailable = 1600

    class respawnView(DynAccessor):
        __slots__ = ()
        additionalTip = 1571
        additionalTipLimited = 1572
        classNotAvailable = 1579
        cooldownLbl = 1573
        destroyedLbl = 1574
        disabledLbl = 1575
        emptySlotInfo = 1577
        emptySlotInfoTooltip = 1578
        nextVehicleName = 1576
        title = 1570

    class rewardWindow(DynAccessor):
        __slots__ = ()

        class base(DynAccessor):
            __slots__ = ()
            btnLabel = 1646
            descText = 1645
            headerText = 1644
            subHeaderText = 1643

        class twitch0(DynAccessor):
            __slots__ = ()
            btnLabel = 1650
            descText = 1649
            headerText = 1647
            subHeaderText = 1648

        class twitch1(DynAccessor):
            __slots__ = ()
            btnLabel = 1654
            descText = 1653
            headerText = 1651
            subHeaderText = 1652

        class twitch2(DynAccessor):
            __slots__ = ()
            btnLabel = 1658
            descText = 1657
            headerText = 1655
            subHeaderText = 1656

        winHeaderText = 1642

    class scorePanel(DynAccessor):
        __slots__ = ()
        mySquadLbl = 1585
        playerScore = 1586
        squadLbl = 1584

    class shells_kinds(DynAccessor):
        __slots__ = ()
        ARMOR_PIERCING = 1227
        ARMOR_PIERCING_CR = 1229
        ARMOR_PIERCING_HE = 1228
        HIGH_EXPLOSIVE = 1226
        HOLLOW_CHARGE = 1225
        params = 1230
        stunParams = 1231

    class siegeMode(DynAccessor):
        __slots__ = ()

        class hint(DynAccessor):
            __slots__ = ()

            class forMode(DynAccessor):
                __slots__ = ()
                c_0 = 1616
                c_1 = 1617
                c_2 = 1618
                c_3 = 1619

            noBinding = 1620
            press = 1615
            wheeled = 1621

    class statistics(DynAccessor):
        __slots__ = ()
        exit = 1194

        class final(DynAccessor):
            __slots__ = ()
            heroes = 1217

            class lifeInfo(DynAccessor):
                __slots__ = ()
                alive = 1218
                dead = 1219

            class personal(DynAccessor):
                __slots__ = ()
                capturePoints = 1215
                damaged = 1210
                directHits = 1213
                directHitsReceived = 1214
                droppedCapturePoints = 1216
                killed = 1209
                postmortem = 1208
                shots = 1212
                spotted = 1211

            class reasons(DynAccessor):
                __slots__ = ()
                reason0 = 1198
                reason1lose = 1200
                reason1tie = 1201
                reason1win = 1199
                reason2 = 1202
                reason3 = 1203

            class stats(DynAccessor):
                __slots__ = ()
                credits = 1206
                experience = 1205
                multipliedExp = 1204
                repair = 1207

            class status(DynAccessor):
                __slots__ = ()
                lose = 1197
                tie = 1195
                win = 1196

        header = 1182

        class headers(DynAccessor):
            __slots__ = ()
            header0 = 1186
            header1 = 1187
            header2 = 1188
            header3 = 1189
            header4 = 1190

        class playerState(DynAccessor):
            __slots__ = ()
            c_0 = 1220
            c_1 = 1222
            c_2 = 1221
            c_3 = 1223
            c_4 = 1224

        class tab(DynAccessor):
            __slots__ = ()

            class line_up(DynAccessor):
                __slots__ = ()
                header = 1170
                title = 1171

            class progressTracing(DynAccessor):
                __slots__ = ()
                notAvailable = 1183

            class quests(DynAccessor):
                __slots__ = ()
                header = 1172

                class notAvailable(DynAccessor):
                    __slots__ = ()
                    title = 1181

                class nothingToPerform(DynAccessor):
                    __slots__ = ()
                    descr = 1179
                    title = 1178

                class status(DynAccessor):
                    __slots__ = ()
                    done = 1176
                    fullDone = 1177
                    inProgress = 1173
                    increaseResult = 1175
                    onPause = 1174

                class switchOff(DynAccessor):
                    __slots__ = ()
                    title = 1180

        class tabs(DynAccessor):
            __slots__ = ()
            group = 1191
            heroes = 1193
            personal = 1192

        team1title = 1184
        team2title = 1185

    class stun(DynAccessor):
        __slots__ = ()
        indicator = 1637
        seconds = 1638

    tabStatsHint = 1598

    class tankmen(DynAccessor):
        __slots__ = ()
        commander = 1048
        driver = 1049
        gunner = 1051
        loader = 1052
        radioman = 1050

    class timer(DynAccessor):
        __slots__ = ()
        battlePeriod = 1284
        started = 1283
        starting = 1282
        waiting = 1281

    class trajectoryView(DynAccessor):
        __slots__ = ()

        class hint(DynAccessor):
            __slots__ = ()
            alternateModeLeft = 1635
            alternateModeRight = 1636
            noBindingKey = 1634

    class vehicle_messages(DynAccessor):
        __slots__ = ()
        DEATH_FROM_DEATH_ZONE_ALLY_SELF = 1484
        DEATH_FROM_DEATH_ZONE_ENEMY_SELF = 1482
        DEATH_FROM_DEATH_ZONE_SELF_SUICIDE = 1480
        DEATH_FROM_DROWNING_ALLY_SELF = 1423
        DEATH_FROM_DROWNING_ENEMY_SELF = 1421
        DEATH_FROM_DROWNING_SELF_SUICIDE = 1419
        DEATH_FROM_FIRE = 1410
        DEATH_FROM_GAS_ATTACK_ALLY_SELF = 1487
        DEATH_FROM_GAS_ATTACK_ENEMY_SELF = 1486
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_ALLY_SELF = 1467
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_ENEMY_SELF = 1465
        DEATH_FROM_INACTIVE_CREW_AT_WORLD_COLLISION_SELF_SUICIDE = 1463
        DEATH_FROM_OVERTURN_ALLY_SELF = 1605
        DEATH_FROM_OVERTURN_ENEMY_SELF = 1604
        DEATH_FROM_OVERTURN_SELF_SUICIDE = 1603
        DEATH_FROM_RAMMING_ALLY_SELF = 1511
        DEATH_FROM_RAMMING_ENEMY_SELF = 1509
        DEATH_FROM_RAMMING_SELF_SUICIDE = 1507
        DEATH_FROM_SHOT = 1360
        DEATH_FROM_SHOT_ARTILLERY = 1363
        DEATH_FROM_SHOT_BOMBER = 1364
        DEATH_FROM_WORLD_COLLISION_ALLY_SELF = 1450
        DEATH_FROM_WORLD_COLLISION_ENEMY_SELF = 1448
        DEATH_FROM_WORLD_COLLISION_SELF_SUICIDE = 1446
        DEVICE_CRITICAL_AT_RAMMING_ALLY_ALLY = 1341
        DEVICE_CRITICAL_AT_RAMMING_ALLY_SELF = 1338
        DEVICE_CRITICAL_AT_RAMMING_ALLY_SUICIDE = 1339
        DEVICE_CRITICAL_AT_RAMMING_ENEMY_ALLY = 1340
        DEVICE_CRITICAL_AT_RAMMING_ENEMY_SELF = 1337
        DEVICE_CRITICAL_AT_RAMMING_SELF_SUICIDE = 1336
        DEVICE_CRITICAL_AT_WORLD_COLLISION_ALLY_ALLY = 1329
        DEVICE_CRITICAL_AT_WORLD_COLLISION_ALLY_SELF = 1326
        DEVICE_CRITICAL_AT_WORLD_COLLISION_ALLY_SUICIDE = 1327
        DEVICE_CRITICAL_AT_WORLD_COLLISION_ENEMY_ALLY = 1328
        DEVICE_CRITICAL_AT_WORLD_COLLISION_ENEMY_SELF = 1325
        DEVICE_CRITICAL_AT_WORLD_COLLISION_SELF_SUICIDE = 1324
        DEVICE_DESTROYED_AT_RAMMING_ALLY_ALLY = 1347
        DEVICE_DESTROYED_AT_RAMMING_ALLY_SELF = 1344
        DEVICE_DESTROYED_AT_RAMMING_ALLY_SUICIDE = 1345
        DEVICE_DESTROYED_AT_RAMMING_ENEMY_ALLY = 1346
        DEVICE_DESTROYED_AT_RAMMING_ENEMY_SELF = 1343
        DEVICE_DESTROYED_AT_RAMMING_SELF_SUICIDE = 1342
        DEVICE_DESTROYED_AT_WORLD_COLLISION_ALLY_ALLY = 1335
        DEVICE_DESTROYED_AT_WORLD_COLLISION_ALLY_SELF = 1332
        DEVICE_DESTROYED_AT_WORLD_COLLISION_ALLY_SUICIDE = 1333
        DEVICE_DESTROYED_AT_WORLD_COLLISION_ENEMY_ALLY = 1334
        DEVICE_DESTROYED_AT_WORLD_COLLISION_ENEMY_SELF = 1331
        DEVICE_DESTROYED_AT_WORLD_COLLISION_SELF_SUICIDE = 1330
        DEVICE_STARTED_FIRE_AT_RAMMING_ALLY_ALLY = 1353
        DEVICE_STARTED_FIRE_AT_RAMMING_ALLY_SELF = 1350
        DEVICE_STARTED_FIRE_AT_RAMMING_ALLY_SUICIDE = 1351
        DEVICE_STARTED_FIRE_AT_RAMMING_ENEMY_ALLY = 1352
        DEVICE_STARTED_FIRE_AT_RAMMING_ENEMY_SELF = 1349
        DEVICE_STARTED_FIRE_AT_RAMMING_SELF_SUICIDE = 1348
        TANKMAN_HIT_AT_WORLD_COLLISION_ALLY_ALLY = 1359
        TANKMAN_HIT_AT_WORLD_COLLISION_ALLY_SELF = 1356
        TANKMAN_HIT_AT_WORLD_COLLISION_ALLY_SUICIDE = 1357
        TANKMAN_HIT_AT_WORLD_COLLISION_ENEMY_ALLY = 1358
        TANKMAN_HIT_AT_WORLD_COLLISION_ENEMY_SELF = 1355
        TANKMAN_HIT_AT_WORLD_COLLISION_SELF_SUICIDE = 1354