"""Tests for the Besen BS20 packet protocol."""

from __future__ import annotations

import pytest

from custom_components.besen_bs20.exceptions import ProtocolError
from custom_components.besen_bs20.protocol import (
    PacketAssembler,
    build_command,
    device_name_bytes,
    parse_login,
    parse_packet,
    parse_single_ac_status,
)


def test_build_and_parse_command() -> None:
    """Command packets include framing, password, command, and checksum."""

    packet = build_command(12345678, "123456", 32770)

    parsed = parse_packet(packet)

    assert parsed.password == b"123456"
    assert parsed.command == 32770
    assert parsed.data == b""
    assert parsed.raw == packet


def test_parse_rejects_bad_checksum() -> None:
    """Checksum mismatches are rejected."""

    packet = bytearray(build_command(12345678, "123456", 32770))
    packet[10] ^= 0xFF

    with pytest.raises(ProtocolError, match="checksum"):
        parse_packet(packet)


def test_packet_assembler_reassembles_fragmented_notifications() -> None:
    """BLE notification fragments are reassembled into full packets."""

    packet = build_command(12345678, "123456", 32771, [1])
    assembler = PacketAssembler()

    assert assembler.feed(packet[:7]) == []
    assert assembler.feed(packet[7:15]) == []
    packets = assembler.feed(packet[15:])

    assert len(packets) == 1
    assert packets[0].command == 32771
    assert packets[0].data == b"\x01"


def test_parse_login_response() -> None:
    """Login parser extracts charger identity and phase count."""

    data = bytearray(69)
    data[0] = 10
    data[1:16] = b"Besen\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    data[17:32] = b"BS20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    data[33:49] = b"HW1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    data[49:53] = bytes([0, 0, 0, 22])
    data[53] = 32
    data[54:69] = b"basic\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    info = parse_login(bytes(data), "12345678")

    assert info["serial"] == "12345678"
    assert info["phases"] == 3
    assert info["manufacturer"] == "Besen"
    assert info["model"] == "BS20"
    assert info["hardware_version"] == "HW1"
    assert info["output_power"] == 22
    assert info["output_max_amps"] == 32


def test_parse_single_ac_status_three_phase() -> None:
    """AC status parser extracts electrical values and charger state."""

    data = bytearray(34)
    data[0] = 1
    data[1:3] = (2300).to_bytes(2, "big")
    data[3:5] = (1600).to_bytes(2, "big")
    data[5:9] = bytes([0, 0, 0, 42])
    data[9:13] = (1234).to_bytes(4, "big")
    data[13:15] = (22500).to_bytes(2, "big")
    data[15:17] = (23000).to_bytes(2, "big")
    data[18] = 4
    data[19] = 1
    data[20] = 14
    data[21:25] = b"\x00\x00\x00\x00"
    data[25:27] = (2310).to_bytes(2, "big")
    data[27:29] = (1000).to_bytes(2, "big")
    data[29:31] = (2320).to_bytes(2, "big")
    data[31:33] = (900).to_bytes(2, "big")

    status = parse_single_ac_status(bytes(data), "12345678")

    assert status["l1_voltage"] == 230.0
    assert status["l1_amperage"] == 16.0
    assert status["inner_temp_c"] == 25.0
    assert status["outer_temp"] == 30.0
    assert status["plug_state"] == "Connected Locked"
    assert status["output_state"] == "Charging"
    assert status["current_state"] == "Completed"
    assert status["charging_status"] == "Finish Charging"
    assert status["charger_status"] is True
    assert status["l2_voltage"] == 231.0
    assert status["l3_amperage"] == 9.0
    assert status["current_energy"] == 8078


def test_device_name_bytes_are_prefixed_and_padded() -> None:
    """Device names are ACP-prefixed and padded to the expected length."""

    payload = device_name_bytes("Garage")

    assert bytes(payload[:10]) == b"ACP#Garage"
    assert len(payload) == 32
    assert payload[-1] == 0
