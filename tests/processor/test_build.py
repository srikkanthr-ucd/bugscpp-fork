import defects4cpp.processor
import defects4cpp.taxonomy

CONFIG_NAME = ".defects4cpp.json"


def test_check_build_attr():
    commands = defects4cpp.processor.CommandList()
    assert "build" in commands


def test_build_fixed(dummy_config, gitenv):
    d = dummy_config("test_build_fixed")

    checkout = defects4cpp.processor.CheckoutCommand()
    build = defects4cpp.processor.BuildCommand()
    project = "yara"
    index = 1
    checkout_dir = d / project / f"fixed#{index}"

    checkout(f"{project} {index} --target {str(d)}".split())
    assert (checkout_dir / CONFIG_NAME).exists()

    build(f"{str(checkout_dir)} --quiet".split())
    assert not list(checkout_dir.glob("**/*.gcno"))


def test_build_fixed_with_coverage(dummy_config, gitenv):
    d = dummy_config("test_build_fixed_with_coverage")

    checkout = defects4cpp.processor.CheckoutCommand()
    build = defects4cpp.processor.BuildCommand()
    project = "yara"
    index = 1
    checkout_dir = d / project / f"fixed#{index}"

    checkout(f"{project} {index} --target {str(d)}".split())
    assert (checkout_dir / CONFIG_NAME).exists()

    build(f"{str(checkout_dir)} --coverage --quiet".split())
    assert list(checkout_dir.glob("**/*.gcno"))


def test_build_buggy(dummy_config, gitenv):
    d = dummy_config("test_build_buggy")

    checkout = defects4cpp.processor.CheckoutCommand()
    build = defects4cpp.processor.BuildCommand()
    project = "yara"
    index = 1
    checkout_dir = d / project / f"buggy#{index}"

    checkout(f"{project} {index} --buggy --target {str(d)}".split())
    assert (checkout_dir / CONFIG_NAME).exists()

    build(f"{str(checkout_dir)} --quiet".split())
    assert not list(checkout_dir.glob("**/*.gcno"))


def test_build_buggy_with_coverage(dummy_config, gitenv):
    d = dummy_config("test_build_buggy_with_coverage")

    checkout = defects4cpp.processor.CheckoutCommand()
    build = defects4cpp.processor.BuildCommand()
    project = "yara"
    index = 1
    checkout_dir = d / project / f"buggy#{index}"

    checkout(f"{project} {index} --buggy --target {str(d)}".split())
    assert (checkout_dir / CONFIG_NAME).exists()

    build(f"{str(checkout_dir)} --coverage --quiet".split())
    assert list(checkout_dir.glob("**/*.gcno"))
