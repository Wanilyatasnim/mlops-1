# Cleanup Notes

## Files to Remove (Old Structure)

The following files/directories are from the old structure and can be removed:

1. `src/app/` - Old monolithic app (replaced by services/)
2. `src/train.py` - Moved to `training/train.py`
3. `Dockerfile` (root) - Removed (each service has its own)

## New Structure

- ✅ `services/` - All microservices
- ✅ `training/` - ML training scripts
- ✅ `docs/` - All documentation
- ✅ `terraform/` - Infrastructure as Code
- ✅ `tests/` - Test files

## Migration Complete

All files have been reorganized. The project now follows a clean microservices structure.

