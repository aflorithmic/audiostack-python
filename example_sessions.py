#!/usr/bin/env python3
"""
Example script demonstrating AudioStack Sessions SDK usage.

This script shows how to use the AudioStack Sessions SDK to create, manage,
and work with sessions in the AudioStack system.
"""

import os
from uuid import UUID

import audiostack
from audiostack.projects.project import Project, Session

# Configure AudioStack
audiostack.api_base = os.environ.get("AUDIO_STACK_DEV_URL", "https://v2.api.audio")
audiostack.api_key = os.environ["AUDIO_STACK_DEV_KEY"]  # type: ignore


def main():
    """Main example function."""
    print("AudioStack Sessions SDK Example")
    print("=" * 40)

    # Create a project first
    print("\n1. Creating a project...")
    project = Project.create(projectName="Sessions Example Project")
    print(f"   Created project: {project.projectName} (ID: {project.projectId})")

    project_id = UUID(project.projectId)

    # Create a session
    print("\n2. Creating a session...")
    session = Session.create(
        projectId=project_id,
        workflowId="example_workflow_123",
        sessionName="My Test Session",
        status="active",
        state={
            "user_preferences": {"voice": "en-US", "speed": 1.0},
            "progress": {"step": 1, "total_steps": 5},
        },
    )
    print(f"   Created session: {session.sessionName} (ID: {session.sessionId})")

    session_id = UUID(session.sessionId)

    # Get the session
    print("\n3. Retrieving the session...")
    retrieved_session = Session.get(projectId=project_id, sessionId=session_id)
    print(f"   Retrieved session: {retrieved_session.sessionName}")
    print(f"   Status: {retrieved_session.status}")
    print(f"   State: {retrieved_session.state}")

    # List all sessions for the project
    print("\n4. Listing all sessions...")
    sessions = Session.list(projectId=project_id)
    print(f"   Found {len(sessions.sessions)} sessions")
    for s in sessions.sessions:
        print(f"   - {s.sessionName} ({s.status})")

    # Update the session
    print("\n5. Updating the session...")
    updated_session = Session.update(
        projectId=project_id,
        sessionId=session_id,
        status="completed",
        state={
            "user_preferences": {"voice": "en-US", "speed": 1.0},
            "progress": {"step": 5, "total_steps": 5},
            "completion_time": "2024-01-01T12:00:00Z",
        },
    )
    print(f"   Updated session status to: {updated_session.status}")

    # List sessions with workflow filter
    print("\n6. Listing sessions with workflow filter...")
    filtered_sessions = Session.list(
        projectId=project_id, workflowId="example_workflow_123"
    )
    print(f"   Found {len(filtered_sessions.sessions)} sessions with workflow filter")

    # Clean up - delete the session
    print("\n7. Cleaning up...")
    Session.delete(projectId=project_id, sessionId=session_id)
    print("   Session deleted")

    print("\nExample completed successfully!")


if __name__ == "__main__":
    main()
