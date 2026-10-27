"""Transport placeholders preserve unavailable capability truth."""
import pytest

from hardware_service.fpga_transport import SerialFpgaTransport, UsbSpiFpgaTransport


def test_serial_and_usb_spi_adapters_never_fake_hardware_success():
    for transport in [SerialFpgaTransport(), UsbSpiFpgaTransport()]:
        assert transport.available is False
        with pytest.raises(RuntimeError) as caught:
            transport.exchange(b'control', timeout_s=1)
        assert caught.value.code == 'HARDWARE_UNAVAILABLE'


@pytest.mark.parametrize('frame,timeout', [(b'', 1), ('control', 1), (b'control', 0),
    (b'control', True), (b'control', float('nan'))])
def test_unavailable_transport_still_rejects_invalid_exchange_configuration(frame, timeout):
    with pytest.raises(RuntimeError) as caught:
        SerialFpgaTransport().exchange(frame, timeout_s=timeout)
    assert caught.value.code == 'INVALID_CONFIGURATION'
