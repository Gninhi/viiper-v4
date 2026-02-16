"""
Skill Loader for dynamic loading and auto-registration.

Discovers and loads skills from the skills package.
"""

import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import List, Type
from viiper.skills.base import Skill
from viiper.skills.registry import SkillRegistry


class SkillLoader:
    """
    Dynamic skill loader.

    Auto-discovers and registers skills from the skills package.
    """

    @staticmethod
    def load_from_module(module_name: str) -> int:
        """
        Load all skills from a Python module.

        Args:
            module_name: Module to load from (e.g., 'viiper.skills.frontend')

        Returns:
            Number of skills loaded

        Example:
            SkillLoader.load_from_module('viiper.skills.frontend')
        """
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            return 0

        count = 0

        # Inspect module for Skill subclasses
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Skip if not a Skill subclass
            if not issubclass(obj, Skill):
                continue

            # Skip base Skill class itself
            if obj is Skill:
                continue

            # Skip abstract classes
            if inspect.isabstract(obj):
                continue

            # Register skill
            try:
                SkillRegistry.register(obj)
                count += 1
            except Exception:
                # Skip skills that fail to register
                pass

        return count

    @staticmethod
    def load_from_package(package_name: str) -> int:
        """
        Load all skills from a package and its subpackages.

        Args:
            package_name: Package to load from (e.g., 'viiper.skills')

        Returns:
            Total number of skills loaded

        Example:
            SkillLoader.load_from_package('viiper.skills')
        """
        try:
            package = importlib.import_module(package_name)
        except ImportError:
            return 0

        total = 0

        # Get package path
        if hasattr(package, '__path__'):
            package_path = package.__path__
        else:
            return 0

        # Walk through all modules in package
        for importer, modname, ispkg in pkgutil.walk_packages(
            path=package_path, prefix=package_name + "."
        ):
            # Skip __pycache__ and other special modules
            if modname.endswith('__pycache__'):
                continue

            # Load skills from this module
            count = SkillLoader.load_from_module(modname)
            total += count

        return total

    @staticmethod
    def load_all_skills() -> int:
        """
        Load all skills from the viiper.skills package.

        Returns:
            Total number of skills loaded

        Example:
            # Load all skills at startup
            count = SkillLoader.load_all_skills()
            print(f"Loaded {count} skills")
        """
        # Load from each sub-package
        subpackages = [
            'viiper.skills.frontend',
            'viiper.skills.backend',
            'viiper.skills.devops',
            'viiper.skills.testing',
            'viiper.skills.data',
        ]

        total = 0
        for pkg in subpackages:
            try:
                count = SkillLoader.load_from_package(pkg)
                total += count
            except Exception:
                # Skip packages that don't exist yet
                pass

        return total

    @staticmethod
    def load_skill_file(file_path: Path) -> int:
        """
        Load skills from a specific Python file.

        Args:
            file_path: Path to Python file containing skill

        Returns:
            Number of skills loaded

        Example:
            SkillLoader.load_skill_file(Path('custom_skill.py'))
        """
        # Convert file path to module name
        # This is complex and may not work in all cases
        # For now, we'll focus on package-based loading
        raise NotImplementedError("File-based loading not yet implemented")

    @staticmethod
    def reload_all() -> int:
        """
        Clear registry and reload all skills.

        Returns:
            Number of skills loaded

        Example:
            # Reload skills (useful during development)
            count = SkillLoader.reload_all()
        """
        SkillRegistry.clear()
        return SkillLoader.load_all_skills()

    @staticmethod
    def validate_skill(skill_class: Type[Skill]) -> List[str]:
        """
        Validate a skill class.

        Args:
            skill_class: Skill class to validate

        Returns:
            List of validation errors (empty if valid)

        Example:
            errors = SkillLoader.validate_skill(MySkill)
            if errors:
                print("Validation failed:", errors)
        """
        errors = []

        try:
            # Try to instantiate
            skill = skill_class()

            # Check required attributes
            if not skill.metadata:
                errors.append("Missing metadata")

            if not skill.metadata.name:
                errors.append("Missing metadata.name")

            if not skill.metadata.slug:
                errors.append("Missing metadata.slug")

            # Check slug format (kebab-case)
            if skill.metadata.slug:
                import re
                if not re.match(r'^[a-z0-9-]+$', skill.metadata.slug):
                    errors.append("Slug must be kebab-case (lowercase, hyphens only)")

            # Check generate method exists
            if not hasattr(skill, 'generate') or not callable(skill.generate):
                errors.append("Missing generate() method")

            # Try calling generate with empty context
            try:
                result = skill.generate({})
                if not isinstance(result, dict):
                    errors.append("generate() must return Dict[str, str]")
            except NotImplementedError:
                errors.append("generate() not implemented")
            except Exception as e:
                errors.append(f"generate() raised error: {str(e)}")

        except Exception as e:
            errors.append(f"Failed to instantiate: {str(e)}")

        return errors
