"""Installed RPC bindings carry genuine bounded NCAP with coherent metadata."""
import json

import grpc
import pytest

from contracts.capture_codec import decode_digital
from contracts.generated import rpc_v2_pb2 as pb
from contracts.generated import rpc_v2_pb2_grpc as rpc
from hardware_service.server import build_server
from hardware_service.station.physical import PhysicalHardwareStation


def read_reply(evidence):
    class CaptureFixture(PhysicalHardwareStation):
        # Data-plane fixture only: not a production physical driver.
        def read_capture(self):
            return evidence

    server = build_server({'capture': CaptureFixture('capture')})
    port = server.add_insecure_port('127.0.0.1:0')
    assert port
    server.start()
    try:
        with grpc.insecure_channel(f'127.0.0.1:{port}') as channel:
            return rpc.HardwareServiceStub(channel).ReadCapture(
                pb.Target(station_id='capture', experiment_id='e'), timeout=10)
    finally:
        server.stop(0).wait()


@pytest.mark.parametrize('signal', ['y', 'long_' + 's' * 256])
def test_100k_capture_crosses_default_rpc_limit_losslessly_as_ncap(signal):
    samples = [{'signal': signal, 'time_ns': i, 'value': 'X' if i % 3 == 2 else i % 2}
               for i in range(100000)]
    reply = read_reply({'available': True, 'duration_ns': 100000, 'samples': samples})
    assert reply.accepted and reply.code == pb.OK
    metadata = json.loads(reply.result_json)
    assert 'samples' not in metadata and len(reply.result_json) < 1000
    assert reply.capture_payload.startswith(b'NCAP')
    assert len(reply.capture_payload) <= 9 + 65536 + 100000 * 11
    decoded = decode_digital(reply.capture_payload)
    assert decoded['samples'] == samples
    assert decoded['duration_ns'] == metadata['duration_ns'] == 100000
    assert metadata['sample_count'] == len(decoded['samples'])


def test_driver_sample_count_cannot_create_inconsistent_metadata():
    reply = read_reply({'available': True, 'duration_ns': 1, 'sample_count': 99,
                        'samples': [{'signal': 'y', 'time_ns': 0, 'value': 1}]})
    assert reply.accepted
    assert json.loads(reply.result_json)['sample_count'] == 1
    assert len(decode_digital(reply.capture_payload)['samples']) == 1


@pytest.mark.parametrize('evidence', [
    {'available': 1, 'samples': []}, {'available': True, 'samples': {}},
    {'available': False, 'samples': [{'signal': 'y', 'time_ns': 0, 'value': 1}]},
    {'available': True, 'duration_ns': 1, 'samples': [{'signal': 'y', 'time_ns': 0, 'value': 2}]},
    {'available': True, 'duration_ns': True, 'samples': []},
])
def test_malformed_driver_capture_never_produces_binary_success(evidence):
    reply = read_reply(evidence)
    assert not reply.accepted and reply.code == pb.DRIVER_ERROR
    assert not reply.capture_payload
